import collections

class Weighter(collections.MutableMapping):
	def __init__(self, data={}, base=1.0):
		self.base = float(base)
		self.memo = data.copy()
		self.total = sum(data.values())
	
	def __getitem__(self, k):
		return self.memo[k] * self.base / self.total
	
	def __setitem__(self, k, v):
		self.total += v - self.memo.get(k, 0)
		self.memo[k] = v
	
	def __delitem__(self, k):
		del self.memo[k]
	
	def __len__(self):
		return len(self.memo)
	
	def __iter__(self):
		for k in self.memo:
			yield k

if __name__ == '__main__':
	d = {
		'a' : 111, 
		'b' : 222,
	}
	w = Weighter(d)
	w['aa'] = 111
	w['bb'] = 222
	w['bb'] = 111
	print(w['a'])
	print(w['b'])
	print(w['aa'])
	print(w['bb'])
	for k, v in w.items():
		print('%s\t%s' % (k , v))
	print(sum(w.values()))
	print(dict(w))
