'''
Project 1 - COMP 479
Bryce Hamilton 40050171
Due: October 8, 2021
'''

# -- IMPORTS --

# nltk for text processing
import nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# regular expressions for parsing and cleaning
import re


# file writing helpers
from helpers.file_writers import write_str_to_file, write_list_to_file

# may be required to redownload the following libaries
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


# -- GLOBAL VARIABLES --

# intialize porter stemmer
ps = PorterStemmer()

# create set of english stop words from nltk for default stop words list
nltk_stop_words = set(stopwords.words('english'))


# -- PIPELINE FUNCTIONS --

# STEP 1
def read_smg(file_paths):
    '''
    Generator of smg file contents.
    Given a list of paths to reuters smg files, 
    reads in each and yields the file number and document contents.
    
    Parameters:
        file_paths (List[str]): list of file path strings to Reuters smg files
    
    Yields:
        file_num (str): The number of the file that was read, from 0 - 21
        file_content (str): The entire contents of the file
    '''
    # filter out non-sgm files
    for file_path in file_paths:
        if not file_path.endswith(".sgm"):
            continue
        
        # open file
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        
            # read file
            file_content = f.read() 
            
            # parse file number
            file_name = file_path.split('.')[0]
            file_num = file_name[-2:]
            
            yield file_num, file_content


# STEP 1.1
def segment_documents(sgm_file):
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
    
    for doc in documents:
        
        # find doc id
        doc_id = re.findall(doc_id_regex, doc, flags=re.DOTALL)[0]
        
        # find text in document
        doc_text = re.findall(body_regex, doc, flags=re.DOTALL)[0]

        yield doc_id, doc_text

# STEP 1.2
def extract_html_symbols(document_str):
    '''
    Removes html symbols from document string using regex.
    
    Parameters:
        document_str (str): Content of document
    
    Returns:
        document_str (str): The content of the same document with html symbols removed
    '''
    # match any sequence starting with '&' ending with ';'
    html_symbol_regex = r'(&.+;)'
    
    # replace all with white space
    document_str = re.sub(html_symbol_regex, " ", document_str)
    
    return document_str

# STEP 1.3
def extract_punctuation(document_str):
    '''
    Removes non-alphabetic characters 
    and replaces linebreaks with white space from document string using regex.
    
    Parameters:
        document_str (str): Content of document
    
    Returns:
        document_str (str): The content of the same document without 
                            non-alphabetic characters or linebreaks 
    '''
    # replace linebreaks with white space
    document_str = re.sub(r"\n", " ", document_str)
    
    # replace '/' with whitespace
    document_str = re.sub(r"/", " ", document_str)
    
    # remove non alphabetic characters
    document_str = re.sub(r'[^A-Za-z ]+', '', document_str)

    return document_str


# STEP 1.3 VARIANT
def extract_punctuation_keep_digits(document_str):
    '''
    Removes non-alphanumeric characters 
    and replaces linebreaks with white space from document string using regex.
    
    Parameters:
        document_str (str): Content of document
    
    Returns:
        document_str (str): The content of the same document without 
                            non-alphanumeric characters or linebreaks 
    '''
    # replace linebreaks with spaces
    document_str = re.sub(r"\n", " ", document_str)
    
    # replace '/' with whitespace
    document_str = re.sub(r"/", " ", document_str)
    
    # remove non-alphanumeric characters
    document_str = re.sub(r'[^A-Za-z0-9 ]+', '', document_str)

    return document_str


# STEP 2
def tokenize_doc_str(doc_id, document_str):
    '''
    Tokenizes document string using nltk, 
    includes document id with token.
    
    Parameters:
        doc_id (str): The id of the document passed
        document_str (str): Content of document
    
    Returns:
        (List[(str, str)]): List of tuples, each with doc id and token
                            
    '''
    return [(doc_id, token) for token in word_tokenize(document_str)]


# STEP 3
def case_fold_tokens(token_tuples):
    '''
    Case folds list of token tuples
    Preserves document id with token.
    
    Parameters:
        token_tuples (List[(str, str)]): List of tuples, each with doc id and token
    
    Returns:
        (List[(str, str)]): List of tuples, each with doc id and lower case token
                            
    '''
    return [(doc_id, token.lower()) for doc_id, token in token_tuples]


# STEP 4
def stem_tokens(token_tuples):
    '''
    Stems list of token tuples with nltk Porter Stemmer.
    Preserves document id with token.
    
    Parameters:
        token_tuples (List[(str, str)]): List of tuples, each with doc id and token
    
    Returns:
        (List[(str, str)]): List of tuples, each with doc id and stemmed token
                            
    '''
    return [(doc_id, ps.stem(token)) for doc_id, token in token_tuples]


# STEP 5
def filter_out_stop_words(token_tuples, stop_words):
    '''
    Removes stop words from token tuples.
    Preserves document id with token.
    
    Parameters:
        token_tuples (List[(str, str)]): List of tuples, each with doc id and token
    
    Returns:
        (List[(str, str)]): List of tuples, each with doc id and token
                            
    '''
    return [(doc_id, token) for doc_id, token in token_tuples if token not in stop_words]



# -- MAIN --

def run(file_names, doc_limit_per_file, stop_words=nltk_stop_words):
    '''
    Runs pipeline.
    
    Parameters:
        file_names (List[str]): List of file path strings to Reuters sgm files
        doc_limit_per_file (int): Limit to number of documents that should be processed per file
        stop_words (List[str]): List of stop words strings to be used to filter final token list
    
    Returns:
        None
                            
    '''
    # step 1
    for file_num, file_content in read_smg(file_names):
        
        # track number of doc's process and written to output
        doc_count = 1
        
        # step 1.1
        for doc_id, doc in segment_documents(file_content):
            
            # check if doc limit for writing output files is reached
            if doc_count > doc_limit_per_file:
                break
            
            # step 1.2
            doc = extract_html_symbols(doc)
            
            # step 1.3
            doc = extract_punctuation(doc)
            
            # write output of step 1
            write_str_to_file(file_num, doc_count, 1, doc)
            
            
            # step 2
            doc_tokens = tokenize_doc_str(doc_id, doc)
            
            # write output of step 2
            write_list_to_file(file_num, doc_count, 2, doc_tokens)

            
            # step 3
            lower_case_tokens = case_fold_tokens(doc_tokens)
            
            # write output of step 3
            write_list_to_file(file_num, doc_count, 3, lower_case_tokens)
            
            
            # step 4
            stemmed_lower_case_tokens = stem_tokens(lower_case_tokens)
            
            # write output of step 4
            write_list_to_file(file_num, doc_count, 4, stemmed_lower_case_tokens)
            
            
            # step 5
            filter_stemmed_lower_case_tokens = filter_out_stop_words(stemmed_lower_case_tokens, stop_words)
            
            # write output of step 5
            write_list_to_file(file_num, doc_count, 5, filter_stemmed_lower_case_tokens)

            # increment doc count
            doc_count += 1
    