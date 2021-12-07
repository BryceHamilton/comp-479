import os
from bs4 import BeautifulSoup
import re


def read_files(file_paths):
    for file_name, file_path in file_paths:            
        # open file
        with open(file_path, 'r') as f:

            # parse title from file
            doc_title =  file_name.split('.html')[0]
        
            # read file
            file_content = f.read() 
            
            yield doc_title, file_content

def main():
    HTML_DIR = "docs_html"
    TEXT_DR = "docs_txt"
    
    html_file_paths = [(file_name, os.path.join(HTML_DIR, file_name)) for file_name in os.listdir(HTML_DIR)]
    
    for doc_title, html_file in read_files(html_file_paths):
        soup = BeautifulSoup(html_file, 'html.parser')
        
        doc_text = soup.get_text().replace('\n', ' ').strip()
        doc_text = re.sub(' +', ' ', doc_text)

        file_name = f"{doc_title}.txt"
        file_path = os.path.join(TEXT_DR, file_name)
        
        with open(file_path, 'w') as f:
            f.write(doc_text)

        print(f"extracted text from {doc_title}")





if __name__ == '__main__':
    main()

