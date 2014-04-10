def binary_search(f, xs, xt, midx, y_lefter, x_close_enough):
	def iter(xl, xu, yl, yu, y):
		#print xl, xu
		if x_close_enough(xl, xu):
			return [xl, xu]
		else:
			xm = midx(xl, xu)
			ym = f(xm)
			if y_lefter(y, ym):
				return iter(xl, xm, yl, ym, y)
			else:
				return iter(xm, xu, ym, yu, y)
	def r(y):
		return iter(xs, xt, f(xs), f(xt), y)
	return r

def disperse_binary_search(f, xs, xt, y_lefter):
	def midx(x0, x1): return (x0 + x1) // 2
	def x_close_enough(x0, x1): return x1-x0 <= 1
	return binary_search(f, xs, xt, midx, y_lefter, x_close_enough)

def array_binary_search(arr, **argd):
	key = argd.get('key', (lambda it: it))
	reverse = argd.get('reverse', False)
	arr_l = float('inf') if reverse else -float('inf')
	arr_u = -arr_l
	def f(i):
		return arr_l if i == -1 else arr_u if i == len(arr) else key(arr[i])
	if reverse:
		def y_lefter(y0, y1): return y0 > y1
	else:
		def y_lefter(y0, y1): return y0 < y1
	def midx(x0, x1): return (x0 + x1) // 2
	def x_close_enough(x0, x1): return x1-x0 <= 1
	return binary_search(f, -1, len(arr), midx, y_lefter, x_close_enough)

#testabs = array_binary_search([1.1 , 2.2 , 3.3 , 4.4]) #, value=(lambda i: i))
#testabs2 = array_binary_search([4.4 , 3.3 , 2.2 , 1.1] , reverse = True)
#print [[y , testabs(y)] for y in [0 , 1.1 , 2 , 2.2 , 3 , 3.3 , 4 , 4.4 , 5]]

