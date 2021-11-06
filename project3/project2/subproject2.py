'''
Project 2 - COMP 479
Bryce Hamilton 40050171
Subproject 2

run from command line: 

    - query processor
    `python subproject2 {query}`
    Where {query} is desired query term

    - query processor validation
    `python subproject2 qval`
    Validates queries in 'queries_to_validate.json'

    - document retrieval for manual validation
    `python subproject2 doc {doc_id}`
    Where {doc_id} is the document id of document to be retrieved

    Example validation flow:
    
    - run `python subproject2 apple`

    - result: query found in all 2 documents
    ['1361', '20872']

    - run `python subproject2 doc 1361`

    - result: doc 1361

    - find 'apple' in doc

    - etc

'''

# -- IMPORTS --

import sys
import json 
import re

# -- GLOBAL VARIABLES --

# read initial inverted index
index = json.load(open('indexes/index.json', 'r'))

# -- QUERY PROCESSOR --
def query_processor(query):
    '''
    Search index for query
    Parameters:
        query (str): Query to be processed
    Returns
        result (None or [int, [str]]): 
            - None if query not found
            - [int, [str]] term frequency and posting list, (doc ids)
    '''
    if query not in index:
        print('Query not in index')
        return None
    return index[query]


def validator(query):
    '''
    Validate query processor
    Parameters:
        query (str): Query to be processed
    Returns
        result (None or [int, [str]]): 
            - None if query not found
            - [int, [str]] term frequency and posting list, (doc ids)
    Throws Error:
        If document returned from query processor does not contain query
    '''
    result = query_processor(query)
    
    if result is None:
        return None
    
    freq, doc_ids = result
    
    for doc_id in doc_ids:
        confirm(query, doc_id)
    
    return result

def confirm(query, doc_id):
    '''
    Confirm that a given document includes a query term
    '''
    document = get_document(doc_id)
    assert query in document, "query not found in document"


def get_document(doc_id):
    '''
    Retrieve a document given a document id
    '''

    # find file number
    file_num = int(doc_id) // 1000

    # parse file number sufix for file path
    file_num_str = str(file_num) if file_num > 9 else '0' + str(file_num)

    # define path to file
    file_path = 'reuters21578/reut2-0' + file_num_str + '.sgm'
   
    # open reuters file
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        
        # read file
        file_content = f.read() 

        doc_regex = r'<REUTERS.* NEWID="' + doc_id + r'">(.*?)</REUTERS>'

        document = re.findall(doc_regex, file_content, flags=re.DOTALL)[0]

        body_regex = r"<BODY>(.*?)</BODY>"

        document_body = re.findall(body_regex, document, flags=re.DOTALL)[0]

        return document_body


def three_query_validation():
    '''
    Validate queries from file
    '''

    # read queries
    queries = json.load(open('queries/queries_to_validate.json', 'r'))

    # validate each query
    for query in queries:
        print('validating query ' + str(query))
        result = validator(query)
        
        if result is None:
            print('query "' + str(query) + '" not found in index')
        
        else:
            freq, docs = result
            print('query "' + str(query) + '" found in ' + str(freq) + ' documents:')
            print(docs)
    
    return 'queries ' + str(queries) + ' all validated'


# -- DRIVER --

if __name__ == '__main__':

    if len(sys.argv) == 1:
        sys.exit('please enter a query term')
    
    # parse first command line arg
    arg = sys.argv[1]
    
    # print doc based on doc id
    if arg == 'doc':
        doc_id = sys.argv[2]
        
        if doc_id is None:
            print('Please enter doc id')
            sys.exit(0)
            
        sys.exit(get_document(doc_id))

    elif arg == 'qval':
        sys.exit(three_query_validation())

    else: 
        # get posting list of query
        query = arg
        
        result = validator(query)

        if result:
            freq, doc_ids = result
            print('query found in all ' + str(freq) + ' documents')
            print(doc_ids)

    sys.exit(0)
