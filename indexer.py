from html.parser import HTMLParser
from collections import defaultdict, Mapping, namedtuple
import tokenize, nltk, json, re, os, bs4, string
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

    #TODO remove. Function is for debugging
    def record_dict(self, ddict):
        infile = open("index_dict.txt", "w")
        for key in ddict:
            infile.write("{}:\n".format(key))
        infile.close()

    def create_index(self):
        doc_id_string = "{}.{}"
        special_char_table = str.maketrans(string.punctuation, " " * len(string.punctuation))

        #for debugging
        count = 0    #TODO remove
        #looping through all infiles using the bookkeeping index json
        for infile_coord in self.book_keeping:
            count += 1    #TODO remove
            index_pair = infile_coord.split("/")
            with open((self.rootDir + "/{}/{}").format(index_pair[0], index_pair[1])) as infile:
                tree = BeautifulSoup(infile, 'html.parser').prettify()
                raw = BeautifulSoup(tree, 'html.parser').get_text()
                tokens = word_tokenize(raw)
                for token in tokens:
                    #stemming all tokens
                    stem_token = self.LS.stem(token)
                    if not stem_token:
                        break

                    # remove special characters and split at the resulting whitespace
                    for split_token in stem_token.translate(special_char_table).split():
                        #checks to see if token has other/duplicate postings
                        if split_token in self.index.keys():
                            #Flag to check if duplicate has been found
                            duplicate = False
                            for old_post in self.index[split_token]:
                                #if duplicate posting, create new posting with incnremented term_freq
                                if old_post.doc_id == doc_id_string.format(index_pair[0], index_pair[1]):
                                    up_term_freq = old_post.term_freq + 1
                                    tf_idf = self.calculate_tf_idf(up_term_freq, len(self.index[split_token]), len(tokens), len(self.book_keeping))
                                    new_post = self.Posting(old_post.doc_id, up_term_freq, tf_idf, old_post.url)
                                    self.index[split_token].remove(old_post)
                                    duplicate = True
                                    break
                            #no duplicate fouond, therefore create new posting and reset duplicate flag
                            if not duplicate:
                                new_post = self.Posting(doc_id_string.format(index_pair[0], index_pair[1]), 1, 0, self.book_keeping[infile_coord])
                                duplicate = False
                        else:
                            new_post = self.Posting(doc_id_string.format(index_pair[0], index_pair[1]), 1, 0, self.book_keeping[infile_coord])
                        self.index[split_token].append(new_post)
                        self.index[split_token].sort(key=lambda x:x.tf_idf, reverse=True)            

            #if count == 10:    #TODO remove
            #    break
        #self.record_dict(self.index)    #TODO remove

    

