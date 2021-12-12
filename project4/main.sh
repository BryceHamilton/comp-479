#! /bin/bash

[ -d "docs_html" ] && rm -rf "docs_html"
[ -d "docs_txt" ] && rm -rf "docs_txt"

mkdir "docs_html"
mkdir "docs_txt"

echo "RUNNING CRAWLER" > "demo.txt"
echo -e "\n" >> "demo.txt"

python3 crawler.py $1

num_docs=$(find docs_html -type f | wc -l)

echo "SAVED $num_docs FILES" >> "demo.txt"
echo -e "\n" >> "demo.txt"

echo "RUNNING EXTRACTOR" >> "demo.txt"
echo -e "\n" >> "demo.txt"

python3 extract_text.py >> "demo.txt"
echo -e "\n" >> "demo.txt"

echo "RUNNING CLUSTERING" >> "demo.txt"
echo -e "\n" >> "demo.txt"

python3 cluster.py >> "demo.txt"
echo -e "\n" >> "demo.txt"

echo "RUNNING KEYWORDS" >> "demo.txt"
echo -e "\n" >> "demo.txt"

python3 keywords.py >> "demo.txt"
echo -e "\n" >> "demo.txt"

echo "RUNNING SENTIMENT ANALYSIS" >> "demo.txt"
echo -e "\n" >> "demo.txt"

python3 sentiment_analysis.py >> "demo.txt"
echo -e "\n" >> "demo.txt"

echo "DONE" >> "demo.txt"