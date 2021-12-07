import os
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
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
#     idf_df = idf_df.sort_values('TF-IDF', ascending=False)        
    
    return tfidf_df


def cluster(k, doc_titles, docs):
    vectorizer = TfidfVectorizer(stop_words={'english'})
    X = vectorizer.fit_transform(docs)
    
    model = KMeans(n_clusters=k, init='k-means++', max_iter=200, n_init=10)
    model.fit(X)
    labels = model.labels_

    clusters = list(zip(doc_titles, labels, docs))

    return pd.DataFrame(clusters, columns=['doc_title','cluster', 'doc'])

def print_clusters(k, clusters_df):
    for cluster_num in range(k):

        print('Cluster: {}'.format(cluster_num))

        cluster = clusters_df[clusters_df.cluster == cluster_num]
        
        text = cluster["doc"]
        text = text.str.cat(sep=' ').lower()
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
                
        print('Titles')
        titles = cluster['doc_title']         
        print(titles.to_string(index=False))

        with open(f"clusters/{k}/{cluster_num}.txt", 'w') as f:
                f.write(titles.to_string(index=False))
        
        # plt.figure()
        # plt.imshow(wordcloud, interpolation="bilinear")
        # plt.axis("off")
        # plt.show()

def kmeans_cluster(k, doc_titles, docs):
    clusters_df = cluster(k, doc_titles, docs)
    print_clusters(k, clusters_df)
    return clusters_df

def main():
    TEXT_DIR = "docs_txt"
    doc_titles, docs = get_text_files(TEXT_DIR)

    tfidf_df = get_tfidf(docs)
    
    k = 3
    clusters_df = kmeans_cluster(k, doc_titles, docs)
    sentiment_analysis(k, clusters_df, tfidf_df)
    
#     k = 6
#     clusters_df = kmeans_cluster(k, doc_titles, docs)
#     sentiment_analysis(k, clusters_df, tfidf_df)

if __name__ == "__main__":
    main()