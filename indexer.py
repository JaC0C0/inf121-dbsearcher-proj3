from html.parser import HTMLParser
from collections import defaultdict, Mapping, namedtuple
import tokenize, nltk, json, re, os, bs4
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer

# Title: namedtuple and default values for optional keyword arguments
# Author: Mark Lodato
# Date: 12/9/15
# Code version: <code version>
# Availability: https://stackoverflow.com/questions/11351032/namedtuple-and-default-values-for-optional-keyword-arguments
def namedtuple_with_defaults(typename, field_names, default_values=()):
    T = namedtuple(typename, field_names)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    if isinstance(default_values, Mapping):
        prototype = T(**default_values)
    else:
        prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T



class indexer():
	def __init__(self, rootDir):
		self.rootDir = rootDir
		print("Indexer Created")
		nltk.download('punkt')
		self.Posting = namedtuple_with_defaults('Posting', 'doc_id, term_freq, tf_idf, url', ["", 0, 0, ""])
		self.LS = LancasterStemmer()
		self.index = defaultdict(int)
		self.book_keeping = json.load(open(self.rootDir + '/bookkeeping.json'))

	def display_dict(self, ddict):
		for key in ddict:
			print("{}: {}".format(key, ddict[key]))

	def create_index(self):
    	#for debugging
		count = 0
		for line in self.book_keeping:
			count += 1
			pair = line.split("/")
			first = int(pair[0]) 
			second = int(pair[1])
			file = open((self.rootDir + "/{}/{}").format(first, second))
			raw = BeautifulSoup(file, 'html.parser').get_text()
			tokens = word_tokenize(raw)
			for token in tokens:
				self.index[self.LS.stem(token)] += 1
				# print(token)
			if count == 10:
				break
			self.display_dict(self.index)

	
if __name__ == "__main__":
	rootDir = 'WEBPAGES/WEBPAGES_RAW'
	the_indexer = indexer(rootDir)
	the_indexer.create_index()
	print ("Exiting program")
