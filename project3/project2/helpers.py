'''
Project 1 - COMP 479
Bryce Hamilton 40050171

helpers.py contains tweaked pipeline functions from Project 1
notably: segment_documents() call other pipeline functions 
and is to be used as input for subproject1
'''

# -- IMPORTS --

# nltk for text processing
import nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


# regular expressions for parsing and cleaning
import re

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# may be required to redownload the following libaries
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


# -- GLOBAL VARIABLES --

# intialize porter stemmer
ps = PorterStemmer()

# create set of english stop words from nltk for default stop words list
# nltk_stop_words = set(stopwords.words('english'))

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
        f = open(file_path, 'r')
        
        # read file
        file_content = f.read() 
        
        # parse file number
        file_name = file_path.split('.')[0]
        file_num = file_name[-2:]
        
        yield file_num, file_content

        f.close()


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

            yield doc_id, [token for token in doc_text.split(" ")]
            
        except:
            doc_no_body_count += 1
    
    print(str(doc_no_body_count) + ' documents without body')

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