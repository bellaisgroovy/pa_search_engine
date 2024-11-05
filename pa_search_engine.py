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
def sanitize_word(word):
    """
    Removes all non ascii characters from a given word
    """
    new_word = ""

    lowercase_ascii = set(string.ascii_lowercase)

    for letter in word.lower():
        if letter in lowercase_ascii:
            new_word += letter

    return new_word


# %%----------------------------------------------------------------------------
def parse_line(line):
    """    
    Parses a given line, 
    removes whitespaces, splits into list of sanitize words
    """

    dirty_list_of_words = _convert_to_no_whitespace_list(line)

    return _sanitize_list(dirty_list_of_words)


def _convert_to_no_whitespace_list(line):
    line = line.strip()
    return line.split(" ")


def _sanitize_list(dirty_list_of_words):
    list_of_words = []

    for dirty_word in dirty_list_of_words:
        sanitized_word = sanitize_word(dirty_word)

        if len(sanitized_word) > 0:
            list_of_words.append(sanitized_word)

    return list_of_words


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
        _update_forward_index(document, forward_index)
        _update_term_freq()
    # <YOUR-CODE-HERE>

    end = timer()
    print("Time taken to index file: ", filename, " = ", end - start)


def _update_forward_index(document, forward_index):
    words = _create_set_of_all_words_in(document)

    for word in words:
        is_present_in = forward_index.get(word)
        forward_index[word] = _amend_or_create(given_set = is_present_in, new_item = document.name)


def _amend_or_create(given_set, new_item):
    if given_set:
        given_set.add(new_item)
        return given_set
    else:
        return {new_item}


def _update_term_freq(document, term_freq):
    word_set = _create_set_of_all_words_in(document)
    word_list = _create_list_of_all_words_in(document)
    total_words = len(word_list)

    for word in word_set:
        word_occurrences = _occurrence_count(word, word_list)

        term_freq[word] = word_occurrences / total_words


def _occurrence_count(search_item, array):
    count = 0
    for item in array:
        if item == search_item:
            count += 1

    return count


def _create_list_of_all_words_in(document):
    document.seek(0)

    return parse_line(document.read())


def _create_set_of_all_words_in(document):
    return set(_create_list_of_all_words_in(document))


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

    words = parse_line(search_phrase)
    result = {}

    # <YOUR-CODE-HERE>
    sorted_result = []

    return (sorted_result)
