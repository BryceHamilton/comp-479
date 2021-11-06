'''
Project 2 - COMP 479
Bryce Hamilton 40050171
Subproject 3

run from command line: 
`python subproject3`
See output in '/results'
'''

# -- IMPORTS --

import sys
import json
from nltk.stem import PorterStemmer

from tabulate import tabulate

# -- GLOBAL VARIABLES --

# read initial inverted index
init_index = json.load(open('indexes/index.json', 'r'))

# intialize porter stemmer
ps = PorterStemmer()

# -- HELPERS -- 

def dict_size(index):
    return len(index.keys())

def token_size(index):
    return sum([len(lst) for freq, lst in index.values()])


# PART 2 and 4 helper
def intersect(lst1, lst2):
    '''
    Return the set intersection of two sorted lists
    Parameters:
        lst1 ([str]): Sorted posting list of doc ids
        lst2 ([str]): Sorted posting list of doc ids
    Returns
        lst3 ([str]): Sorted intersection of lst1 and lst2
    '''
    return sorted(list(set(lst1 + lst2)))


# to be run sequentially for each compression technique
def compress(index, technique, init_dict_size, init_tokens_size):
    '''
    Apply a Compression technique
    Record and print results
    Parameters:
        index ({term (str): p_list: [str]}): Initial inverted index 
    Returns
        index ({term (str): p_list: [str]}): Compressed Inverted index
    '''
    # record inital dict and token sizes
    current_dict_size = dict_size(index)
    current_tokens_size = token_size(index)

    # compress index
    index = technique(index)

    # record new dict, tokens sizes
    new_dict_size = dict_size(index)
    new_tokens_size = token_size(index)

    # compute change in size percentage
    delta_dict = (1 - (new_dict_size / current_dict_size)) * 100 * -1
    delta_tokens = (1 - (new_tokens_size / current_tokens_size)) * 100 * -1

    # compute total change in size percentage
    total_change_dict = (1 - (new_dict_size / init_dict_size)) * 100 * -1
    total_change_tokens = (1 - (new_tokens_size / init_tokens_size)) * 100 * -1

    # store results
    results = [new_dict_size, delta_dict, total_change_dict,
                new_tokens_size, delta_tokens, total_change_tokens
                ]

    # return compressed index and results
    return index, results

# -- COMPRESSION FUNCTIONS --

# PART 1
def remove_numbers(index):
    '''
    Compression technique, 
    removing numbers from index dictionary and posting lists
    Parameters:
        index ({term (str): p_list: [str]}): Initial inverted index 
    Returns
        index ({term (str): p_list: [str]}): Inverted index without numbers
    '''
    return {k: v for k, v in index.items() if not k.isnumeric()}

# PART 2
def case_fold(index):
    '''
    Compression technique, 
    Case folding terms
    Parameters:
        index ({term (str): p_list: [str]}): Initial inverted index 
    Returns
        index ({term (str): p_list: [str]}): Case folded inverted index
    '''

    # iterate over each term
    for term in list(index):

        term_lower = term.lower()

        # term is already case folded, do nothing
        if term_lower == term:
            continue
        
        # term is not lowercase, two options
        
        freq, lst = index[term]

        # if lowercase term not in index, set to term posting list
        if term_lower not in index:
            index[term_lower] = index[term]
        
        # otherwise, merge with lowercase posting list
        elif term_lower in index:
            lower_freq, lower_lst = index[term_lower]
            intersect_list = intersect(lower_lst, lst)
            index[term_lower] = [len(intersect_list), intersect_list]

        # in both cases, delete the non-lowercase posting list after
        del index[term]

    return index

# PART 3
def stop_words_remover(stop_words):
    '''
    Accept a list of stopwords, 
    return a function that accepts an inverted index and filter those stop words 
    '''
    def remove_stop_words(index):
        '''
        Compression Technique
        Filter index for stop words
        '''
        return {k: v for k, v in index.items() if k not in stop_words}

    return remove_stop_words

# DEFINE STOP WORD 30 FUNCTION
stop_words_30 = json.load(open('stop_words/stop_words_30.json', 'r'))
remove_stop_words_30 = stop_words_remover(stop_words_30)

# DEFINE STOP WORD 150 FUNCTION
stop_words_150 = json.load(open('stop_words/stop_words_150.json', 'r'))
remove_stop_words_150 = stop_words_remover(stop_words_30) 

# PART 4
def stem(index):
    '''
    Compression technique
    Stem all terms in the dictionary using Portert Stemmer
    Parameters:
        index ({term (str): p_list: [str]}): Initial inverted index 
    Returns
        index ({term (str): p_list: [str]}): Stemmed inverted index
    '''
    # Similar logic to case_folding

    # iterate over each term
    for term in list(index):

        stemmed_term = ps.stem(term)

        freq, lst = index[term]

        # if stemming doesn't not change the term, do nothing
        if stemmed_term == term:
            continue
        
        # if stemmed term not in index, set to term posting list
        if stemmed_term not in index:
            index[stemmed_term] = index[term]
        
        # otherwise, merge with lowercase posting list
        elif stemmed_term in index:
            stem_freq, stem_lst = index[stemmed_term]
            intersect_list = intersect(stem_lst, lst)
            index[stemmed_term] = [len(intersect_list), intersect_list]

        # in both cases, delete the non-lowercase posting list after
        del index[term]

    return index

# -- DRIVER --

def run_compression():
    '''
    Run each compression technique
    on the inverted index, sequentially
    store the difference in size
    create table and write to file
    '''

    # define compression techniques to iterate over
    techniques = [
        ('remove_numbers', remove_numbers),
        ('case_fold', case_fold),
        ('remove_stop_words_30', remove_stop_words_30),
        ('remove_stop_words_150', remove_stop_words_150),
        ('stem', stem)
        ]

    # store size of initial index 
    init_dict_size = dict_size(init_index)
    init_tokens_size = token_size(init_index)

    # first row of table for initial index
    first_row = ['unfiltered', 
                init_dict_size, '', '',
                init_tokens_size, '', '']

    all_results = [first_row]

    index = init_index

    # compress index with each technique
    for name, technique in techniques:

        print('COMPRESSING with: ' + name)

        # compress
        index, results = compress(index, technique, init_dict_size, init_tokens_size)
        
        # store results
        all_results.append([name] + results)

    # TABLE

    # headers
    headers = ['number', 'Δ%', 'T%']
    table_headers = [' '] + headers + headers

    # create table
    table = tabulate(all_results, headers=headers, tablefmt='orgtbl')

    # major header 
    spacer = '                         '
    terms_header = '--------(distinct)-terms----------------------------'
    posting_header = ' --------nonpositional-posting------------------------'
    major_header = spacer + terms_header + posting_header

    # write table to file
    with open('results/compression.txt', 'w') as f:
        print(major_header, file=f)
        print(table, file=f)

    # store compressed index
    with open('indexes/index_comparison.json', 'w') as f:
        print(index, file=f)
    
    return index

def compare_indexes(index, compressed_index, queries, f):
    '''
    Compare original and compressed index
    Using 3 queries
    Compare results
    '''
    
    # iterate over queries
    for query in queries:

        index_result = []
        compressed_result = []

        # check query results

        compressed_query = ps.stem(query.lower())

        if query not in index:
            print(f'query {query} not found in original index', file=f)
            print('\n', file=f)
        else:
            freq, index_result = index[query]
            print('original index', file=f)
            print(f'query {query}', file=f)
            print(f'found in {freq} docs: {index_result}', file=f)
            print('\n', file=f)
        
        if compressed_query not in compressed_index:
            print(f'query {query} not found in compressed index', file=f)
            print('\n', file=f)
        else:
            freq, compressed_result = compressed_index[compressed_query]
            print('compressed index', file=f)
            print(f'query {query}', file=f)
            print(f'found in {freq} docs: {compressed_result}', file=f)
            print('\n', file=f)

        if set(index_result) == set(compressed_result):
            print('results are equal', file=f)
            print(index_result, file=f)
            print('\n', file=f)

        else:
            index_diff = set(index_result).difference(compressed_result)
            compressed_diff = set(compressed_result).difference(index_result)

            if len(index_diff) != 0:
                print(f'query {query}:', file=f)
                print('not found in compressed', file=f)
                print(f'docs: {index_diff}', file=f)
                print('\n', file=f)
            
            if len(compressed_diff) != 0:
                print(f'query {query}:', file=f)
                print('not found in original', file=f)
                print(f'docs: {compressed_diff}', file=f)
                print('\n', file=f)

    
def main():

    # compress index
    compressed_index = run_compression()
    index = init_index

    # open file writer
    f = open('results/comp_indexes.txt', 'w')

    # validation queries
    queries = json.load(open('queries/queries_to_validate.json', 'r'))
    compare_indexes(index, compressed_index, queries, f)

    # challenge queries
    queries = json.load(open('queries/challenge_queries.json', 'r'))
    compare_indexes(index, compressed_index, queries, f)

    f.close()

if __name__ == '__main__':
    main()
    sys.exit(0)