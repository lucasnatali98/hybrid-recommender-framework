def read(filename):
	f = open(filename, 'r')
	user_ratings = dict()
	for line in f.readlines():
		data = line.split('\t')
		userid = int(data[0])
		ratings = (int(data[1]), float(data[2]))
		if userid not in user_ratings:
			user_ratings[userid] = []
		user_ratings[userid].append(ratings)
	return user_ratings
