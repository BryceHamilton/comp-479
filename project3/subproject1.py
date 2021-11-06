# -*- coding: utf-8 -*-
'''
Project 3 - COMP 479
Bryce Hamilton 40050171
Subproject 1

run from command line: 
`python subproject1`
Part A: See output in command line and results/subproject1
Part B: see output index in 'indexes/index_10000.json'
'''

# -- IMPORTS --

import os
import sys
import json

# for comparing compute time
import time


# helpers from Project 1
from project2.helpers import segment_documents, read_smg

# comparison from Project 2
from project2.subproject1 import naive_indexer


# modified from Project 2 to append directly to posting list
def process_files(index, max_pairs):
    '''
    Initial step to process files and use step 1 to ouput doc_id, token paris
    Parameters:
        F (List[(doc_id, token)]): List of doc_id, token pairs, appended to
    '''

    # gather list of reuters file paths to be processed
    sgm_files = ['reuters21578/' + file_name for file_name in os.listdir('reuters21578')]
    
    # create file stream
    file_stream = read_smg(sgm_files)

    # track the number of (doc_id, term) pairs output
    current_pairs = 0
    
    # iterate over file stream
    for file_num, file in file_stream:
    
        # create doc stream from file, without html and punctuation
        doc_stream = segment_documents(file)

        # iterate over doc stream, where doc = (doc_id, list of tokens)
        for doc_id, token in output_doc_id_term_pairs(doc_stream):
    
            # add doc_id, token pair to index
            if token not in index:
                index[token] = []
            
            if doc_id not in index[token]:
                index[token].append(doc_id)

            current_pairs += 1
            
            if current_pairs == max_pairs:
                print(str(max_pairs) + ' processed')
                return


# PART 1
def output_doc_id_term_pairs(doc_stream):
    '''
    While there are still more documents to be processed, accepts a document as a list
    of tokens and outputs term-documentID pairs to a list F

    Parameters:
        doc_stream (Generator (doc_id: str, token_list: [str])): Stream of documents 
    
    Yields:
        doc_id (str): Id of the document in which the token occurs
        token (str): The instance of a token in the document
    '''
    
    # get first doc from stream
    doc = next(doc_stream, None)

    doc_count = 0

    # keep processing documents while there is input
    while doc is not None:
        doc_id, doc_token_list = doc
        for token in doc_token_list:
            if token != '':

                yield doc_id, token
        doc_count += 1
        doc = next(doc_stream, None)

    print(str(doc_count) + ' documents processed')


def spimi(max_pairs):
    index = dict()
    process_files(index, max_pairs)
    return index

if __name__ == '__main__':
    
    # PART A
    MAX_PAIRS = 10000
    
    s_t0 = time.time()
    SPIMI_index = spimi(MAX_PAIRS)
    s_t1 = time.time()
    
    n_t0 = time.time()
    n_index = naive_indexer(MAX_PAIRS)
    n_t1 = time.time()

    results = ""

    message = 'number of tokens in SPIMI index: ' + str(len(SPIMI_index.keys()))
    print(message)
    results += message
    
    print('\n')
    results += '\n'

    message = 'SPIMI took: ' + str(s_t1 - s_t0)
    print(message)
    results += message
    results += '\n'

    message = 'Naive took: ' + str(n_t1 - n_t0)
    print(message)
    results += message
    results += '\n'
    
    message = 'SPIMI is ' + str((n_t1 - n_t0) / (s_t1 - s_t0)) + ' times faster'
    print(message)
    results += message

    f = open('results/subproject1.txt', 'w')
    f.write(results)
    f.close()

    # PART B
    json.dump(SPIMI_index, open('indexes/index_10000.json', "w", encoding="utf−8"), indent=3)
    sys.exit(0)