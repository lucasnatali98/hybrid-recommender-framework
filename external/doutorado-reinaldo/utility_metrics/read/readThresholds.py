def read(filename):
	f = open(filename, 'r')
	user_thres = dict()
	for line in f.readlines():
		data = line.split(';')
		userid = int(data[0])
		threshold = float(data[1])
		user_thres[userid]= threshold
	return user_thres
