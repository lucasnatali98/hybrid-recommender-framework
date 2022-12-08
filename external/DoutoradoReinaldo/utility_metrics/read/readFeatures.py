def read(filename):
	f = open(filename, 'r')
	featureMap = dict()
	itemMap = dict()
	for line in f.readlines():
		data = line.split('\t')
		itemid = int(data[0])
		featureid = int(data[1])
		if itemid not in itemMap:
			itemMap[itemid] = []
		itemMap[itemid].append(featureid)
		if featureid not in featureMap:
			featureMap[featureid] = []
		featureMap[featureid].append(itemid)
	return (itemMap, featureMap)
