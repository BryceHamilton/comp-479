'''
Project 1 - COMP 479
Bryce Hamilton 40050171
Due: October 8, 2021
'''

import os

base_path = 'output'

def get_output_file_path(file_num, doc_num, step_num):
    
    # define 'file_num' dir path
    file_num_dir = f'file_{file_num}'
    file_num_dir_path = os.path.join(base_path, file_num_dir)
    
    # create 'file_num' dir if does not exist
    if not os.path.isdir(file_num_dir_path):
        os.mkdir(file_num_dir_path)    
    
    # define 'doc_num' dir path
    doc_num_dir = f'doc_{doc_num}'
    doc_num_dir_path = os.path.join(file_num_dir_path, doc_num_dir)
    
    # create 'doc_num' dir if does not exist
    if not os.path.isdir(doc_num_dir_path):
        os.mkdir(doc_num_dir_path) 
        
    # define 'file_num_doc_num_step_num' file path
    file_name = f'{file_num_dir}_{doc_num_dir}_step{step_num}.txt'
    
    # return final path 'file_num/doc_num/file_num_doc_num_step_num.txt'
    return os.path.join(doc_num_dir_path, file_name)


def write_str_to_file(file_num, doc_num, step_num, str_to_write):
    file_path = get_output_file_path(file_num, doc_num, step_num)
    
    with open(file_path, 'w') as f:
        f.write(str_to_write)

        
def write_list_to_file(file_num, doc_num, step_num, list_to_write):
    file_path = get_output_file_path(file_num, doc_num, step_num)
    
    with open(file_path, 'w') as f:
        for item in list_to_write:
            f.write(f'{item}\n')