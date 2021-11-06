'''
Project 2 - COMP 479
Bryce Hamilton 40050171
Subproject 1

run from command line: 
`python subproject1`
See output in 'index.json'
'''

# -- IMPORTS --

import os
import sys
import json

# helpers from Project 1
from helpers import segment_documents, read_smg

# PART 0
def process_files(F):
    '''
    Initial step to process files and use step 1 to ouput doc_id, token paris
    Parameters:
        F (List[(doc_id, token)]): List of doc_id, token pairs, appended to
    '''

    # gather list of reuters file paths to be processed
    sgm_files = ['reuters21578/' + file_name for file_name in os.listdir('reuters21578')]
    
    # create file stream
    file_stream = read_smg(sgm_files)
    
    # iterate over file stream
    for file_num, file in file_stream:
    
        # create doc stream from file
        doc_stream = segment_documents(file)

        # iterate over doc stream, where doc = (doc_id, list of tokens)
        for doc_id, token in output_doc_id_term_pairs(doc_stream):
    
            # add doc_id, token pair to F list
            F.append((doc_id, token))

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

    print(f'{doc_count} documents processed')

# PART 2
def remove_duplicates_and_sort(F):
    '''
    While there are still more documents to be processed, accepts a document as a list
    of tokens and outputs term-documentID pairs to a list F

    Parameters:
        F (List[(doc_id, token)]): List of doc_id, token pairs, appended to
    
    Returns:
        F (List[(doc_id, token)]): List of doc_id, token pairs, appended to
    '''

    # remove duplicates
    print('* REMOVING DUPLICATES FROM F *')
    
    # token count
    print(f'initial token count: {len(F)}')

    F = list(set(F))

    # unique token count
    print(f'unique token count: {len(F)}')

    print('* DONE REMOVING DUPLICATES FROM F *')

    # sort by term
    print('* SORTING F BY TERM AND DOCID *')
    F = sorted(F, key= lambda t: (t[1], int(t[0])))
    print('* DONE SORTING F BY TERM AND DOCID *')

    return F


# PART 3
def invert(F):
    
    print('* GENERATING INVERTED INDEX FROM F *')
    
    index = dict()
    
    # (term, freq) --> [posting list]
    
    freq = 0
    
    for doc_id, term in F:
        
        if term not in index:
            freq = 0
            index[term] = [freq, []]

        
        freq += 1 
        index[term] = [freq, index[term][1] + [doc_id]]

    print('* DONE GENERATING INVERTED INDEX FROM F *')
    
    print(f'number of terms in index: {len(index.keys())}')
    
    return index
        

def naive_indexer():
    
    # initialize F list of (doc_id, term)
    F = []

    # PART 1
    process_files(F)

    # PART 2
    F = remove_duplicates_and_sort(F)

    # PART 3
    index = invert(F)

    return index


if __name__ == '__main__':
    index = naive_indexer()
    json.dump(index, open('indexes/index.json', "w", encoding="utf−8"), indent=3)
    sys.exit(0)