'''
Project 1 - COMP 479
Bryce Hamilton 40050171
Due: October 8, 2021
'''

import sys

from pipeline import run

num_reuter_files = 22

def main():

    # set default args
    file_limit = 1
    doc_limit_per_file = 5
    
    # check for command line args
    
    # first arg is file_limit
    if len(sys.argv) > 1:
        file_limit = int(sys.argv[1])
        
        if file_limit < 0 or file_limit > num_reuter_files - 1:
            print('file limit out of range')
             
    print(f'file limit set to {file_limit}')
    
    # second arg is doc_limit
    if len(sys.argv) > 2:
        doc_limit_per_file = int(sys.argv[2])
    
    print(f'doc limit per file set to {doc_limit_per_file}')
    
    # format file_num helper
    format_file_num = lambda file_num: f'0{file_num}' if file_num < 10 else str(file_num)
    
    # format file_nums in range 0 - file_limit inclusive
    file_nums = [format_file_num(file_num) for file_num in range(file_limit)]
    
    # define file path with file_num
    reuters_files = [f'reuters21578/reut2-0{file_num}.sgm' for file_num in file_nums]

    # run pipeline
    run(file_names=reuters_files, doc_limit_per_file=doc_limit_per_file)
    

if __name__ == '__main__':
    sys.exit(main())