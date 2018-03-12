import indexer
from nltk.stem.lancaster import LancasterStemmer
from nltk import word_tokenize
from functools import reduce
import string
import json

def get_intersect(post_array):
    post_array.sort(key=lambda x:len(x), reverse=False)
    new_array = []
    for posts in post_array[1:]:
        for post in posts:
            if any(x[0] == post[0] for x in post_array[0]):
                new_array.append(post)
    return new_array


def search():
    search_bool = input("Would you like to compile the search indexer? (\'y\'/\'n\')")
    if (search_bool == "y"):
        rootDir = 'WEBPAGES/WEBPAGES_RAW'
        the_indexer = indexer.indexer(rootDir)
        the_indexer.create_index()
    infile = open("dictionary_file.txt", "r")
    the_indexer = json.load(infile)
    print(len(the_indexer))
    special_char_table = str.maketrans(string.punctuation, " " * len(string.punctuation))

    while (True):
        search_input = input("Search: ")
        tokens = word_tokenize(search_input)
        LS = LancasterStemmer()
        set_of_posts = []
        if (len(tokens) > 1):
            for token in tokens:
                for split_token in token.translate(special_char_table).split():
                    stem_input = LS.stem(split_token)
                    set_of_posts.append(the_indexer[stem_input])
            inter_set = get_intersect(set_of_posts)
            if inter_set:
                for posts in inter_set:
                    print(posts[-1])
            else:
                print("No results")
        else:
            stem_input = LS.stem(tokens[0])
            if the_indexer[stem_input]:
                for posts in the_indexer[stem_input]:
                    print(posts[-1])
            else:
                print("No results")
    infile.close()

if __name__ == "__main__":
    search()
    print ("Exiting program")