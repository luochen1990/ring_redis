################### your redis configuration #####################

REDIS_CONF = {
	'group0' : {
		'node0': {
			'capacity': 50 * 1024 ** 2,
			'connection': {
				'host' : '192.168.230.45',
				'port' : 15061,
				'db': 0,
				'socket_timeout': 5e-2, #NOTE: this argument should be choosed carefully depending on your network delay & bandwidth, do some test yourself to findout the expected time(in seconds) needed for your biggest data case.
			},
		},
		'node1': {
			'capacity': 50 * 1024 ** 2,
			'connection': {
				'host' : '192.168.230.46',
				'port' : 15061,
				'db': 0,
				'socket_timeout': 5e-2,
			},
		},
	},
}

############################ useage ##############################

from ring_redis import redis_dict

test = redis_dict(REDIS_CONF['group0'], prefix='test.', expire=20)

test['a'] = 'abc'
print("test['a'] : %s" % (test['a']))

print("len(test) : %s" % (len(test)))
print("test.keys() : %s" % (test.keys()[:100]))
print("'a' in test? : %s" % ('a' in test))
print("'b' in test? : %s" % ('b' in test))

print("test.visit_redis('incr', 'x', 1) : %s" % (test.visit_redis('incr', 'x', 1)))
print("test.get_entry('x') : %s" % (test.get_entry('x')))
print("test.total_hash(test.get_entry('x')) : %s" % (test.total_hash(test.get_entry('x'))))
print("test.alive_hash(test.get_entry('x')) : %s" % (test.alive_hash(test.get_entry('x'))))

print('\nAPI TEST END, GOING TO TEST EJECT & REDISCOVER...')
print('(try to disconnect one redis node and then reconnect it)\n')
import time
time.sleep(5)
keys = ['A', 'B', 'C', 'D']
for k in keys:
	test[k] = '0'
while True:
	print("ALIVE: %s ~ %s" % (len(test.alive_hash.nodes), [(k, test.visit_redis('incr', k), test.total_hash(test.get_entry(k))) for k in keys]))
	time.sleep(0.1)

