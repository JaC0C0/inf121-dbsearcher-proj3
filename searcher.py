import indexer
from nltk.stem.lancaster import LancasterStemmer
from nltk import word_tokenize
from functools import reduce

def get_intersect(post_array):
    post_array.sort(key=lambda x:len(x), reverse=False)
    new_array = []
    for posts in post_array[1:]:
    	for post in posts:
    		if any(x.doc_id == post.doc_id for x in post_array[0]):
    			new_array.append(post)
    return new_array


def search():
	rootDir = 'WEBPAGES/WEBPAGES_RAW'
	the_indexer = indexer.indexer(rootDir)
	the_indexer.create_index()

	while (True):
		search_input = input("Search: ")
		tokens = word_tokenize(search_input)
		LS = LancasterStemmer()
		set_of_posts = []
		if (len(tokens) > 1):
			for token in tokens:
				stem_input = LS.stem(token)
				set_of_posts.append(the_indexer.get_posting(stem_input))
			inter_set = get_intersect(set_of_posts)
			if inter_set:
				for posts in inter_set:
					print(posts.url)
			else:
				print("No results")
		else:
			stem_input = LS.stem(tokens[0])
			if the_indexer.get_posting(stem_input):
				for posts in the_indexer.get_posting(stem_input):
					print(posts.url)
			else:
				print("No results")

if __name__ == "__main__":
	search()
	print ("Exiting program")