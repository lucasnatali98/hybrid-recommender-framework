def read(filename, cutoff=float("inf")):
	f = open(filename, 'r')	
	user_ratings = []
	current_user_id = -1
	try:
		while True:
			line = f.readline().strip()
			if not line: yield (None, None)
			line = line.replace(',', '\t') # alguns arquivos usam ','
			data = line.split('\t')				
			user_id = int(data[0])
			if user_id != current_user_id:
				if current_user_id != -1: yield (current_user_id, user_ratings)
				user_ratings = []
				current_user_id = user_id
			rating = (int(data[1]), float(data[2]))
			if len(user_ratings) < cutoff: user_ratings.append(rating)
	except EOFError:
    		pass
	
	
		
