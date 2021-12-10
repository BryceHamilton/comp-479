import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from sentiment_analysis import sentiment_analysis

def get_text_files(dir):

    text_file_paths = [(file_name, os.path.join(dir, file_name)) for file_name in os.listdir(dir)]

    doc_titles = []
    docs = []
    
    for file_name, file_path in text_file_paths:            
        # open file
        with open(file_path, 'r') as f:

            # parse title from file
            doc_title =  file_name.split('.txt')[0]
        
            # read file
            file_content = f.read() 
            
            doc_titles.append(doc_title)
            docs.append(file_content)

    return doc_titles, docs


def get_tfidf(docs):
    vectorizer = TfidfVectorizer(stop_words={'english'})
    X = vectorizer.fit_transform(docs)

    terms = vectorizer.get_feature_names()

    tfidf_df = pd.DataFrame(X[0].T.todense(), index=terms, columns=["TF-IDF"])    
    tfidf_df = tfidf_df.rename_axis('term').reset_index()
    
    return tfidf_df


def cluster(k, doc_titles, docs):
    vectorizer = TfidfVectorizer(stop_words={'english'})
    X = vectorizer.fit_transform(docs)
    
    model = KMeans(n_clusters=k, init='k-means++', max_iter=200, n_init=10)
    model.fit(X)
    labels = model.labels_

    clusters = list(zip(doc_titles, labels, docs))

    return pd.DataFrame(clusters, columns=['doc_title','cluster', 'doc'])


def kmeans_cluster(k, doc_titles, docs):
    clusters_df = cluster(k, doc_titles, docs)
    print_clusters(k, clusters_df)
    return clusters_df

def main():
    TEXT_DIR = "docs_txt"
    doc_titles, docs = get_text_files(TEXT_DIR)

    tfidf_df = get_tfidf(docs)
    tfidf_df.to_csv("tf_idf.csv")
    
    for k in [3, 6]:
        clusters_df = kmeans_cluster(k, doc_titles, docs)
        clusters_df.to_csv(f"clusters/{k}/clusters_df.csv")

if __name__ == "__main__":
    main()