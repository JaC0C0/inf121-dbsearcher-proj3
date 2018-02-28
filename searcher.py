import indexer
from nltk.stem.lancaster import LancasterStemmer

def search():
	rootDir = 'WEBPAGES/WEBPAGES_RAW'
	the_indexer = indexer.indexer(rootDir)
	the_indexer.create_index()

	while (True):
		search_input = input("Search: ")
		LS = LancasterStemmer()
		stem_input = LS.stem(search_input)
		if the_indexer.get_posting(stem_input):
			for posts in the_indexer.get_posting(stem_input):
				print(posts.url)
		else:
			print("No results")

if __name__ == "__main__":
	search()
	print ("Exiting program")