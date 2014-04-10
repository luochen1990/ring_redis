# -*- coding: utf-8 -*-
import heapq

def merge(*sequences):
    heap = [(seq[0], seq) for seq in sequences]
    heapq.heapify(heap)
    while heap:
        x, seq = heapq.heappop(heap)
        yield seq.pop(0)
        if seq:
            heapq.heappush(heap,  (seq[0], seq))

if __name__ == '__main__':
	A = [[1, 2, 3, 4], [5, 6, 8], [1, (2+1), 5, (3*(3-2)), 7, 9]]
	#B = ([1, 2, 3, 4], [5, 6, 8], [1, (2+1), 5, (3*(3-2)), 7, 9])
	print(list(merge(*A)))
	print(list(merge(*B)))

