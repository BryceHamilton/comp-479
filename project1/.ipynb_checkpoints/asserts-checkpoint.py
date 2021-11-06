'''
Project 1 - COMP 479
Bryce Hamilton 40050171
Due: October 8, 2021
'''

def reader_tests(file_num, file):
    
    assert type(file_num) is str, "file num should be string"
    assert len(file_num) > 0, "file num should not be empty"
    assert int(file_num) >= 0 and int(file_num) <= 22, "file num should be in range"
    
    assert type(file) is str, "file should be a string"
    assert len(file) > 0, "file should not be empty"
    
    
def segmenter_test(doc_id, doc_str):
    
    assert type(doc_id) is str, "doc_id should be string"
    assert len(doc_id) > 0, "doc_id should not be empty"
    assert int(doc_id), "doc_id should be convertable to int"
    
    assert type(doc_str) is str, "doc_str should be a string"
    assert len(doc_str) > 0, "doc_str should not be empty"
    assert "<BODY>" not in doc_str, "doc_str should not include body tags"
    
    
def extractor_test(doc_str):
    
    assert type(doc_str) is str, "doc_str should be a string"
    assert len(doc_str) > 0, "doc_str should not be empty"
    
    for i in range(10):
        assert str(i) not in doc_str, "doc_str should not have digits"
    
    for char in ';:,.[]{}()\|?!@#$%^&*':
        assert char not in doc_str, "doc_str should not have non-alphabetic characters"
        
        

def common_token_tuples_test(token_tuples, test_fns=[]):
    
    assert type(token_tuples) is list
    assert len(token_tuples) > 0, "token_tuples should be non-empty"
    
    for doc_id, token in token_tuples:
        
        assert type(doc_id) is str, "doc_id should be string"
        assert len(doc_id) > 0, "doc_id should not be empty"
        assert int(doc_id), "doc_id should be convertable to int"

        assert type(token) is str, "token should be string"
        assert len(token) > 0, "token should not be empty"
        
        for test_fn in test_fns:
            test_fn(doc_id, token) 
        

def tokenizer_test(token_tuples):
    
    def no_whitespace(doc_id, token):
        assert ' ' not in token, "token should not have whitespace"

    common_token_tuples_test(token_tuples, [no_whitespace])
        
        
def case_folder_test(token_tuples):
    
    def same_as_lower(doc_id, token): 
        assert token.lower() == token, "token should not have uppercase"
    
    common_token_tuples_test(token_tuples, [same_as_lower])
        

def stemmer_test(token_tuples):

    common_token_tuples_test(token_tuples)
    
    # lack of better testing
    

def stop_word_test(token_tuples, stop_words):
    
    def check_stop_words(doc_id, token):
        assert token not in stop_words, "tokens should not include stop words"
        
    common_token_tuples_test(token_tuples, [check_stop_words])