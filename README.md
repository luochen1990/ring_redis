RING REDIS
===

What for:
---

I want a lightweight, High Available & Extensible cache solution using redis, but nutcracker is too heavy for a system with only 2 or 3 application servers and 2 or 3 redis instances. and there isnt a good enough implementation of consistant hash using pure python. so I wrote this. I used it in 2 project and they are running well till now when half a year passed. so I shared it for people who have the same requirement.

Features:
---

- lightweight & pure python solution
- auto eject & rediscover redis nodes
- O(log(slice_number)) time complexity for a consistant hash calculation. (slice_number = max(2000, 200 * node_number))
- O(slice_number * log(slice_number)) time complexity for hash ring rebuilding.
- use O(slice_number) memory space always.

API list:
---

- `redis_dict(redis_confs, prefix='', key=str, expire=None, on_fail=None, on_node_ejected=None, on_node_rediscovered=None, retry_ratio=1e-2, hash_function=crc32)`: construct a redis_dict instance, which can be used as a normal python dict
- `some_redis_dict_instance.visit_redis(cmd, k, args)`: visit lower level redis apis
- `some_redis_dict_instance.get_entry(k)`: return the really redis entry of k
- `some_redis_dict_instance.alive_hash(redis_entry)`: return the node name for redis_entry via alive_hash
- `some_redis_dict_instance.total_hash(redis_entry)`: return the node name for redis_entry via total_hash
- `len(some_redis_dict_instance.alive_hash)`: return the alive nodes number

Install
---

### via pip
```shell
pip install ring_redis
```

### via source code
```shell
cd path/to/ring_redis
python setup.py install
```

How to use:
---

```python
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
print("test['a'] : %s" % (test['a']))

print("len(test) : %s" % (len(test)))
print("test.keys() : %s" % (test.keys()[:100]))
print("'a' in test? : %s" % ('a' in test))
print("'b' in test? : %s" % ('b' in test))

print("test.visit_redis('incr', 'x', 1) : %s" % (test.visit_redis('incr', 'x', 1)))
print("test.get_entry('x') : %s" % (test.get_entry('x')))
print("test.total_hash(test.get_entry('x')) : %s" % (test.total_hash(test.get_entry('x'))))
print("test.alive_hash(test.get_entry('x')) : %s" % (test.alive_hash(test.get_entry('x'))))
```

Notice:
---

- The really redis entry equals to the dict key **only if** `prefix + key(dict_key) == redis_entry`
- The configuration field 'socket_timeout' in REDIS_CONF **should be choosed carefully**, do some test yourself to findout the expected time(in seconds, depending on your network delay & bandwidth) needed for your biggest data case.
- Python built-in function hash is neither consistant nor equally distributed, so **don't use it** as hash_function.
- If non instance of the redis cluster available, exception `RedisClusterUnavailable` will be raised, you should pass `on_fail` as argument of redis_dict constructor or catch this exception to **handler this situation yourself**.

