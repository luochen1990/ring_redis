################### your redis configuration #####################

REDIS_CONF = {
	'group0' : {
		'node0': {
			'capacity': 50 * 1024 ** 2,
			'connection': {
				'host' : '192.168.230.45',
				'port' : 15061,
				'db': 0,
				'socket_timeout': 5e-3,
			},
		},
		'node1': {
			'capacity': 50 * 1024 ** 2,
			'connection': {
				'host' : '192.168.230.46',
				'port' : 15061,
				'db': 0,
				'socket_timeout': 5e-3,
			},
		},
	},
}

############################ useage ##############################

from ring_redis import redis_dict

test = redis_dict(REDIS_CONF['group0'], prefix='test.', expire=20)

test['a'] = 'abc'
test['bc'] = 'def'

print("test['a'] : %s" % (test['a']))
print("test['bc'] : %s" % (test['bc']))

print("len(test) : %s" % (len(test)))
print("test.keys() : %s" % (test.keys()))
print("'a' in test? : %s" % ('a' in test))
print("'b' in test? : %s" % ('b' in test))

print("test.get_entry('x') : %s" % (test.get_entry('x')))
print("test.total_hash(test.get_entry('x')) : %s" % (test.total_hash(test.get_entry('x'))))
print("test.alive_hash(test.get_entry('x')) : %s" % (test.alive_hash(test.get_entry('x'))))
