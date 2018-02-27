import indexer



if __name__ == "__main__":
	rootDir = 'WEBPAGES/WEBPAGES_RAW'
	the_indexer = indexer.indexer(rootDir)
	the_indexer.create_index()
	print ("Exiting program")