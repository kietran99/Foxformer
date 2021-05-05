def foreach(func, iter):
	for e in iter:
		func(e)

add_tuple = lambda tuple_0, tuple_1: (tuple_0[0] + tuple_1[0], tuple_0[1] + tuple_1[1])