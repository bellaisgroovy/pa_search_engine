# -*- coding: utf-8 -*-

"""
Module: 
pa_search_engine

About:
Implements functions used by a directory search engine

SOME FUNCTIONS OR THEIR SKELETONS HAVE BEEN PROVIDED
HOWEVER, YOU ARE FREE TO MAKE ANY CHANGES YOU WANT IN THIS FILE
AS LONG AS IT REMAINS COMPATIBLE WITH main.py and tester.py
"""

# %% ---------------------------------------------------------------------------
# Required Imports
# ------------------------------------------------------------------------------
import string
from timeit import default_timer as timer
import os
import re


# %%----------------------------------------------------------------------------
def dict_to_file(di, fi):
    with open(fi, "w") as f:
        for key, value in di.items():
            f.write("%s:%s\n" % (key, value))


# %%----------------------------------------------------------------------------
def print_result(result):
    """
    Print result (all docs with non-zero weights)
    """
    print("# Search Results:")
    count = 0
    for val in result:
        if val[1] > 0:
            print(val[0])
            count += 1
    print(count, " results returned")


# %%----------------------------------------------------------------------------
def crawl_folder(folder
                 , forward_index
                 , invert_index
                 , term_freq
                 , inv_doc_freq
                 , doc_rank
                 ):
    """"
    Crawls a given folder, and runs the indexer on each file
    """

    total_docs = 0
    for file in os.scandir(folder):
        if file.is_file():
            total_docs += 1
            index_file(file.name, file.path, forward_index, invert_index, term_freq, doc_rank)

    # with invert_index calculated, we can calculate the inv_doc_freq of each unique word
    # where inv_doc_freq = number of documents with the word / total number of documents
    for word in invert_index.keys():
        inv_doc_freq[word] = len(invert_index[word]) / total_docs


# %%----------------------------------------------------------------------------
pattern = re.compile("[^a-z]")


def sanitize_word(word):
    """
    Removes all non ascii characters from a given word
    """
    word = word.lower()
    return pattern.sub("", word)


# %%----------------------------------------------------------------------------
def parse_line(line):
    """    
    Parses a given line, 
    removes whitespaces, splits into list of sanitize words
    """
    # remove whitespace and split into list
    line: list = line.split()

    # convert to lowercase and remove non ascii characters
    clean_line: list = []
    for word in line:
        clean_line.append(sanitize_word(word))

    return clean_line


# %%----------------------------------------------------------------------------
def index_file(filename
               , filepath
               , forward_index
               , invert_index
               , term_freq
               , doc_rank
               ):
    """    
    Given a file, indexes it by calculating its:
        forward_index
        term_freq
        doc_rank
        and updates the invert_index (which is calculated across all files)
    """
    start = timer()


    with open(filepath, 'r', encoding="utf-8") as document:
        # instantiate temporary trackers
        word_occurrences_count = {}  # {word : number of occurences}
        total_words_in_document = 0

        # loop through lines in document
        line = document.readline()
        while line != "":
            line_list = parse_line(line)

            # loop through words in line
            for word in line_list:
                word_occurrences_count[word] = 1 + _get_index_or_default(word_occurrences_count, word, default=0)
                total_words_in_document += 1

                # update forward index
                _add_to_set_in_dict(forward_index, document.name, word)

                # update invert index
                _add_to_set_in_dict(invert_index, word, document.name)

            line = document.readline()

        # update term frequency
        _update_term_freq(term_freq, document.name, word_occurrences_count, total_words_in_document)

        # update document rank
        _update_doc_rank(doc_rank, document.name, total_words_in_document)

    end = timer()
    print("Time taken to index file: ", filename, " = ", end - start)


def _update_doc_rank(doc_rank, name, total):
    doc_rank[name] = 1 / total


def _update_term_freq(term_freq, document_name, occurrences_dict, total):
    # instantiate dictionary for current document
    term_freq[document_name] = {}

    # add term frequency for all words in this document
    for word in occurrences_dict.keys():
        term_freq[document_name][word] = occurrences_dict.get(word) / total


def _get_index_or_default(dictionary, index, default):
    item = dictionary.get(index)

    if item is not None:
        return item
    else:
        return default


def _add_to_set_in_dict(dictionary, index, element):
    set_at_index = dictionary.get(index)

    if set_at_index is not None:
        set_at_index.add(element)
    else:
        dictionary[index] = {element}


# %%----------------------------------------------------------------------------
def search(search_phrase
           , forward_index
           , invert_index
           , term_freq
           , inv_doc_freq
           , doc_rank
           ):
    """    
    For every document, you can take the product of TF and IDF 
    for term of the query, and calculate their cumulative product. 
    Then you multiply this value with that documents document-rank 
    to arrive at a final weight for a given query, for every document. 
    """
    sorted_result = []  # [(doc_name, rank), (doc_name, rank)]

    words: list = parse_line(search_phrase)
    if len(words) == 0:
        return sorted_result

    # for each word get the invert index and get the intersection of it and result
    result: set = invert_index.get(words[0])
    for word in words[1:]:
        result = result.intersection(invert_index[word])#

    if result is None:
        return sorted_result

    # put result in a list of tuples (document, ranking)
    ranking: list = []

    try:
        for document in result:
            # calculate term freq x inverse document freq for each token
            rank = doc_rank.get(document)
            for word in words:
                word_term_freq = term_freq.get(document).get(word)
                word_inv_doc_freq = inv_doc_freq.get(word)
                rank = rank * word_term_freq * word_inv_doc_freq

            ranking.append((document, rank))
    except Exception:
        print(result)
        print(search_phrase)    

    sorted_result = sorted(ranking, key=lambda item: item[1])

    return sorted_result
