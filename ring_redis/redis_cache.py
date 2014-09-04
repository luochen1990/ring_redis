import collections
import logging
import copy
import random
import json
import redis
from .utils.weighter import Weighter
from .utils.hash import crc32
from .consistent_hash import hash_ring

class RedisClusterUnavailable(Exception): pass

try:
	unicode
except NameError:
	unicode = str

class redis_dict(collections.MutableMapping):
	def __init__(self, redis_confs, prefix='', key=str, expire=None, on_fail=None, on_node_ejected=None, on_node_rediscovered=None, retry_ratio=1e-2, hash_function=crc32):
		clients = {k: redis.StrictRedis(**v['connection']) for k, v in redis_confs.items()}
		w = Weighter({k: v['capacity'] for k, v in redis_confs.items()}, max(len(redis_confs)*200, 2000))
		#print clients
		#print dict(w)
		total_hash = hash_ring(nodes = {k: int(v + 1 - 1e-8) for k, v in w.items()}, hash_function=hash_function)
		alive_hash = copy.deepcopy(total_hash)
		#print total_hash
		#print alive_hash
		def _raw_visit_redis(node, cmd, entry, args):
			#print('!!!', node, entry)
			try:
				r = clients[node].__getattribute__(cmd)(entry, *args)
				if self.expire and cmd == 'set':
					clients[node].expire(entry, self.expire)
			except redis.ConnectionError as e:
				if node in alive_hash:
					alive_hash.delete_node(node)
					logging.warn('node "%s" ejected' % node) if not on_node_ejected else on_node_ejected(self, node)
					if len(alive_hash) == 0:
						if on_fail == None:
							raise RedisClusterUnavailable()
						else:
							return on_fail(self)
				raise e
			else:
				if node not in alive_hash:
					alive_hash.insert_node(node, int(w[node] + 1 - 1e-8))
					logging.warn('node "%s" rediscovered' % node) if not on_node_rediscovered else on_node_rediscovered(self, node)
				return r

		def _rec_visit_redis(cmd, entry, args):
			if len(alive_hash):
				node = alive_hash(entry)
				#print('###', node, entry)
				try:
					return _raw_visit_redis(node, cmd, entry, args)
				except redis.ConnectionError as e:
					return _rec_visit_redis(cmd, entry, args)
			else:
				return None

		def get_entry(k):
			entry = prefix + key(k)
			assert type(entry) == unicode or type(entry) == str, 'redis_dict key must be a string or unicode'
			return entry

		def visit_redis(cmd, k, *args):
			entry = get_entry(k)
			if random.random() < retry_ratio:
				node = total_hash(entry)
				try:
					return _raw_visit_redis(node, cmd, entry, args)
				except redis.ConnectionError as e:
					return _rec_visit_redis(cmd, entry, args)
			else:
				return _rec_visit_redis(cmd, entry, args)

		self.prefix = prefix
		self.expire = expire
		self.clients = clients
		self.redis_confs = redis_confs
		self.get_entry = get_entry
		self.alive_hash = alive_hash
		self.total_hash = total_hash
		self.visit_redis = visit_redis

	def __str__(self):
		return '<redis_dict: ' + json.dumps(self.redis_confs, indent=4, sort_keys=True) + '>'

	def __getitem__(self, k):
		return self.visit_redis('get', k)

	def __setitem__(self, k, v):
		assert type(v) == unicode or type(v) == str, 'value must be a string or unicode'
		return self.visit_redis('set', k, v)

	def __delitem__(self, k):
		return self.visit_redis('delete', k)

	def __contains__(self, k):
		return self.visit_redis('exists', k)

	def __len__(self):
		return sum(client.dbsize() for client in self.clients.values())

	def __iter__(self):
		for c in self.clients.values():
			for k in c.keys():
				yield k

	def iteritems(self):
		for c in self.clients.itervalues():
			for k in c.keys():
				yield k, c[k]

	def itervalues(self):
		for c in self.clients.itervalues():
			for k in c.keys():
				yield c[k]

	def items(self):
		return self.items()

	def values(self):
		return self.values()

