import collections
import random
import json
from .utils.hash import crc32
from .utils.binary_search import array_binary_search

class hash_ring(collections.MutableMapping):
	def reload_nodes(self, nodes=None):
		if nodes: self.nodes = nodes
		ring = []
		for k, v in self.nodes.items():
			random.seed(k)
			for i in range(v):
				ring.append((k, self.hashf(random.random())))
		random.seed()
		ring.sort(key = (lambda it: it[1]))
		g = array_binary_search(ring, key = (lambda it: it[1]))
		def search(y):
			xl, xu = g(y)
			return ring[xl][0]
		self.search = search

	def __init__(self, **conf):
		self.hashf = conf.get('hash_function', crc32)
		self.nodes = conf.get('nodes', {})
		self.reload_nodes()

	def __call__(self, key):
		hashv = self.hashf(key)
		return self.search(hashv)

	def insert_node(self, node_id, node_v):
		if node_v != self.nodes.get(node_id, 0):
			self.nodes[node_id] = node_v
			self.reload_nodes()

	def delete_node(self, node_id):
		if node_id in self.nodes:
			del self.nodes[node_id]
			self.reload_nodes()

	def __getitem__(self, node_id):
		return self.nodes[node_id]

	def __setitem__(self, node_id, node_v):
		self.insert_node(node_id, node_v)

	def __delitem__(self, node_id):
		self.delete_node(node_id, node_v)

	def __contains__(self, node_id):
		return node_id in self.nodes

	def __len__(self):
		return len(self.nodes)

	def __iter__(self):
		return iter(self.nodes)

	def full_config(self):
		return {
			'hash_function' : self.hashf,
			'nodes' : self.nodes,
		}

	def __str__(self):
		return '<hash_ring: ' + json.dumps({'nodes': self.nodes, 'hash_function': str(self.hashf)}, indent=4, sort_keys=True) + '>'

