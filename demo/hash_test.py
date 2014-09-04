import random
from ring_redis import hash_ring

import collections
conf = {
	#'hash_function': (lambda x: int(hashlib.md5(str(x)).hexdigest(), 16)) ,
	'nodes': {
		'node1': 1000,
		'node2': 1000,
		'node3': 1000,
	}
}
conf2 = {
	'nodes': {
		'node1': 1000,
		'node3': 1000,
	}
}
conf3 = {
	'nodes': {
		'node1': 1000,
		'node3': 1000,
		'node2': 1000,
	}
}
conf4 = {
	'nodes': {
		'node1': 1000,
		'node3': 1000,
		'node2': 1000,
		'node4': 1000,
	}
}
chash = hash_ring(**conf)
chash2 = hash_ring(**conf2)
chash3 = hash_ring(**conf3)
chash4 = hash_ring(**conf4)
print(chash)
#import copy
#ch = copy.deepcopy(chash)
#del ch['node1']
#print chash, ch
 
items = [(random.random()) for i in range(10000)]
print('Total Keys: %s'% len(items))

c = collections.Counter()
for x in items:
	c[chash(x)] += 1
print('Key Distribution: %s'% c)

rst = set((x, chash(x)) for x in items)
#print sorted(rst)
rst2 = set((x, chash2(x)) for x in items)
#print sorted(rst2)
rst3 = set((x, chash3(x)) for x in items)
#print sorted(rst3)
rst4 = set((x, chash4(x)) for x in items)
#print sorted(rst4)

same12 = rst.intersection(rst2)
print('Consistant Key Number after node2 ejected: %s (2/3 expected)'% len(same12))

same13 = rst.intersection(rst3)
print('Consistant Key Number when node2 come back: %s (1/1 expected)'% len(same13))

same14 = rst.intersection(rst4)
print('Consistant Key Number when new node4 added: %s (3/4 expected)'% len(same14))

