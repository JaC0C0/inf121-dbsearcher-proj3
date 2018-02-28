from html.parser import HTMLParser
from collections import defaultdict, Mapping, namedtuple
import tokenize, nltk, json, re, os, bs4
from math import log10
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
		self.index = defaultdict(list)
		self.book_keeping = json.load(open(self.rootDir + '/bookkeeping.json'))

	def get_posting(self, stem_token):
		return (self.index[stem_token])

	def calculate_tf_idf(self, term_freq, num_doc_term, total_tokens, total_docs):
		tf = term_freq / total_tokens
		idf = log10(total_docs/num_doc_term)
		return(tf*idf)

	#TODO remove
	def record_dict(self, ddict):
		file = open("index_dict.txt", "w")
		for key in ddict:
			file.write("{}:\n".format(key))
			for post in ddict[key]:
				file.write("{}\n".format(post))
			# print(key)
		file.close()

	def create_index(self):
    	#for debugging
		count = 0	#TODO remove
		#looping through all files using the bookkeeping index json
		for file_coord in self.book_keeping:
			count += 1	#TODO remove
			index_pair = file_coord.split("/")
			file = open((self.rootDir + "/{}/{}").format(index_pair[0], index_pair[1]))
			tree = BeautifulSoup(file, 'html.parser').prettify()
			raw = BeautifulSoup(tree, 'html.parser').get_text()
			tokens = word_tokenize(raw)
			#stemming all tokens
			for token in tokens:
				stem_token = self.LS.stem(token)
				#checks to see if token has other/duplicate postings
				if stem_token in self.index.keys():
					#Flag to check if duplicate has been found
					duplicate = False
					for old_post in self.index[stem_token]:
						#if duplicate posting, create new posting with incnremented term_freq
						if old_post.doc_id == "doc{}{}".format(index_pair[0], index_pair[1]):
							up_term_freq = old_post.term_freq + 1
							new_post = self.Posting(
								old_post.doc_id, up_term_freq, self.calculate_tf_idf(
									up_term_freq, len(self.index[stem_token]), len(tokens), len(self.book_keeping)), old_post.url)
							self.index[stem_token].remove(old_post)
							duplicate = True
							break
					#no duplicate
					if (not duplicate):
						new_post = self.Posting("doc{}{}".format(index_pair[0], index_pair[1]), 1, 0, self.book_keeping[file_coord])
						duplicate = False
				else:
					new_post = self.Posting("doc{}{}".format(index_pair[0], index_pair[1]), 1, 0, self.book_keeping[file_coord])
				self.index[stem_token].append(new_post)
				self.index[stem_token].sort(key=lambda x:x.tf_idf, reverse=True)			

			if count == 10:	#TODO remove
				break
		self.record_dict(self.index)

	

