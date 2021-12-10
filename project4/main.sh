#! /bin/bash

[ -d "docs_html" ] && rm -rf "docs_html"
[ -d "docs_txt" ] && rm -rf "docs_txt"

mkdir "docs_html"
mkdir "docs_txt"

python3 crawler.py $1

num_docs=$(find docs_html -type f | wc -l)
echo "saved $num_docs files"

python3 extract_text.py

python3 cluster.py 

python3 keywords.py 

python3 sentiment_analysis.py

