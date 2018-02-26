from html.parser import HTMLParser
from collections import defaultdict
from collections import namedtuple
import tokenize
import ntlk
import json

book_keeping = json.load(open('WEBPAGES/WEBPAGES_RAW/bookkeeping.json'))
Posting = namedtuple('Posting', 'doc_id, term_freq, tf_idf, url')


class indexer():
    # searchIndex = defaultdict()
    for line in book_keeping:
    	print(json.dumps(book_keeping[line]))
    # def generate_posting


if __name__ == "__main__":
    indexer()
    print ("Exiting program")
