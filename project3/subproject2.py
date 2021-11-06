'''
Project 3 - COMP 479
Bryce Hamilton 40050171
Subproject 2

run from command line: 
first run:
`python subproject1` to create indexes (only needed once)
See output in '/indexes'

query processing
run:
`python subproject1 0` to run 4 test queries
`python subproject1 1` to input single keyword query
`python subproject1 2` to input query for BM25 ranked retrieval
`python subproject1 3` to input query for AND unranked
`python subproject1 4` to input query for OR unranked

'''

# -- IMPORTS --

import json
import sys
import os
import re
from math import log10

# helper from Project 1
from project2.helpers import read_smg, extract_html_symbols, extract_punctuation_keep_digits
from project2.subproject2 import query_processor


# STEP 1.1 of Project 1
def segment_documents(sgm_file, doc_length_index):
    '''
    Generator that segments the documents from an sgm_file string.
    
    Parameters:
        sgm_file (str): Content of sgm file
    
    Yields:
        doc_id (str): Id of latest the document parsed from the file
        doc_text (str): Contents of latest the document parsed from the file
    '''
    # define regexes
    doc_regex = r"<REUTERS.*?>.*?</REUTERS>"
    body_regex = r"<BODY>(.*?)</BODY>"
    doc_id_regex = r'NEWID="(.*?)"'
    
    # find all documents in file
    documents = re.findall(doc_regex, sgm_file, flags=re.DOTALL)
    
    doc_no_body_count = 0

    for doc in documents:
        
        # find doc id
        doc_id = re.findall(doc_id_regex, doc, flags=re.DOTALL)[0]
        
        # find text in document
        try:
            doc_text = re.findall(body_regex, doc, flags=re.DOTALL)[0]
            
            # clean doc string
            doc_text = extract_html_symbols(doc_text)

            doc_text = extract_punctuation_keep_digits(doc_text)
            
            # split doc string into tokens
            tokens = doc_text.split(" ")
            
            # extra information for Project 3.2 (document length)
            doc_length_index[doc_id] = len(tokens)

            yield doc_id, [token for token in tokens]
            
        except:
            doc_no_body_count += 1
    
    print(f'{doc_no_body_count} documents without body')



# modified from Project 2 to append directly to posting list
def process_files(index, doc_length_index):
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
    
        # create doc stream from file, without html and punctuation
        doc_stream = segment_documents(file, doc_length_index)

        # iterate over doc stream, where doc = (doc_id, list of tokens)
        for doc_id, token in output_doc_id_term_pairs(doc_stream):
    
            # add doc_id, token pair to index
            if token not in index:
                index[token] = []
            
            # keep duplicate doc_id for term frequency
            index[token].append(doc_id)


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


def spimi_with_duplicates():
    index = dict()
    doc_length_index = dict()
    process_files(index, doc_length_index)
    return index, doc_length_index


def generate_term_freq_index(index):
    term_freq_index = dict()
    
    for term, doc_list in index.items():
        term_freq_per_doc = dict()        
        for doc_id in doc_list:
            if doc_id not in term_freq_per_doc:
                term_freq_per_doc[doc_id] = 0
            term_freq_per_doc[doc_id] = term_freq_per_doc[doc_id] + 1
        
        for doc_id in term_freq_per_doc:
            term_freq_index[(term, doc_id)] = term_freq_per_doc[doc_id]
    
    return term_freq_index


def remove_duplicate_docs(index):
    for term in index:
        index[term] = sorted(list(set(index[term])), key=lambda x: int(x))


def create_probabilistic_indexes():

    # create SPIMI index, keeping duplicate occurences of term in doc
    index, doc_length_index = spimi_with_duplicates()

    print('CREATED DOC LENGTH INDEX')

    # create term frequency index using duplicate docs in posting list
    term_freq_index = generate_term_freq_index(index)
    
    print('CREATED TERM FREQUENCY INDEX')
    
    # remove duplicate docs from index
    remove_duplicate_docs(index)

    print('CREATED INDEX')
    
    json.dump(index, open('indexes/index.json', "w", encoding="utf−8"), indent=3)
    json.dump(doc_length_index, open('indexes/doc_length_index.json', "w", encoding="utf−8"), indent=3)
    term_freq_index = {k[0] + ' ' + k[1]: v for k, v in term_freq_index.items()}
    json.dump(term_freq_index, open('indexes/term_freq_index.json', "w", encoding="utf−8"), indent=3)


# read stored indexes
index = json.load(open('indexes/index.json', 'r'))
doc_length_index = json.load(open('indexes/doc_length_index.json', 'r'))
term_freq_index = json.load(open('indexes/term_freq_index.json', 'r'))
term_freq_index = {(k.split(' ')[0], k.split(' ')[1]): v for k, v in term_freq_index.items()}


def get_average_doc_length(doc_length_index):
    return sum(doc_length_index.values()) / len(doc_length_index.values())


def BM25_ranked_search(query):

    k1, b = 1.6, 0.75
    
    # average document length in collection
    avgDL = get_average_doc_length(doc_length_index)

    # number of documents
    N = len(doc_length_index.keys())

    def IDF(term):
        numerator = N - len(index[term]) + 0.5
        denominator = len(index[term]) + 0.5
        return log10((numerator / denominator) + 1)

    # document frequency is length of posting list

    docs = AND_processor(query)

    scores = []
    
    for doc_id in docs:
        for term in query.split(" "):
            idf = IDF(term)
            term_freq = term_freq_index[(term, doc_id)]
            D = doc_length_index[doc_id]
            numerator = term_freq * (k1 + 1)
            denominator = term_freq + (k1 * ((1-b) + (b * D / avgDL)))

            if denominator == 0:
                scores.append((doc_id, idf * numerator))
            else:
                scores.append((doc_id, idf * (numerator / denominator)))

    results = sorted(scores, key=lambda x: x[1])
    
    return [res[0] for res in results]

    

def single_term_processor(term):
    if term not in index:
        print('term not found')
    else:
        return index[term]


def OR_processor(query):
    query = extract_punctuation_keep_digits(query)
    terms = query.split(" ")
    results = dict()
    for term in terms:
        for doc_id in index[term]:
            results[doc_id] = True
    return list(results.keys())


def intersect(l1, l2):
    if l1 is None:
        return l2
    return [elem for elem in l1 if elem in l2]

def AND_processor(query):
    query = extract_punctuation_keep_digits(query)
    terms = query.split(" ")
    curr_list = None
    for term in terms:
        post_list = index[term]
        curr_list = intersect(curr_list, post_list)
    return curr_list


def run_test_queries():

    single_keyword = 'apple'

    # Part (a)
    print('RUNNING SINGLE KEYWORD COMPARISON FOR: ' + single_keyword)

    print('SPIMI results')
    results = single_term_processor(single_keyword)
    print(results)

    print('original index results')
    results = query_processor(single_keyword)
    print(results)

    # Part (b)
    print('RUNNING TEST QUERIES FOR BM25')

    queries = [
        "Democrats’ welfare and healthcare reform policies",
        "Drug company bankruptcies",
        "George Bush"
        ]
    
    print('queries: ')
    
    for query in queries:
        print(query)
        results = BM25_ranked_search(query)
        print(results)
    
    # Part (c)
    print('RUNNING TEST QUERIES FOR AND UNRANKED')

    queries = [
        "Democrats’ welfare and healthcare reform policies",
        "Drug company bankruptcies",
        "George Bush"
        ]
    print('queries: ')
    
    for query in queries:
        print(query)
        results = AND_processor(query)
        print(results)
   
    # Part (d)
    print('RUNNING TEST QUERIES FOR OR UNRANKED')
    queries = [
        "Democrats’ welfare and healthcare reform policies",
        "Drug company bankruptcies",
        "George Bush"
        ]
    print('queries: ')
    
    for query in queries:
        print(query)
        results = OR_processor(query)
        print(results)

if __name__ == '__main__':

    if len(sys.argv) == 1:
        create_probabilistic_indexes()
        sys.exit(0)

    # parse first command line arg
    arg = sys.argv[1]

    if arg == '0':
        run_test_queries()
        sys.exit(0)


    query_processors_names = {'1': 'single_term_processor',
                        '2': 'BM25_ranked_search',
                        '3': 'AND_processor',
                        '4': 'OR_processor'
                        }

    query_processors = {'1': single_term_processor,
                        '2': BM25_ranked_search,
                        '3': AND_processor,
                        '4': OR_processor
                        }


    print('query processor: ' + query_processors[arg])
    query = input('Input query:\n')

    results = query_processors[arg](query)

    print('results for query: ' + query)
    print(results)

    sys.exit(0)
