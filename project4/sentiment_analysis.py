import pandas as pd
from afinn import Afinn
from nltk import word_tokenize
from nltk.corpus import stopwords

afinn = Afinn()
stop_words = stopwords.words('english')

def sent_score(df):
    return afinn.score(df)

def cluster_keywords(cluster_doc, tfidf_df):
    cluster_tfidf = tfidf_df[tfidf_df['term'].isin(cluster_doc)]
    cluster_tfidf = cluster_tfidf.sort_values('TF-IDF', ascending=False)
    print(cluster_tfidf.head(5))
    return cluster_tfidf['term'].head(50).tolist()

def not_stop(token):
    return token not in stop_words

def find_keywords(df, tfidf_df):

    cluster_corpus = df.groupby("cluster")["doc"]\
            .apply(' '.join)\
            .apply(word_tokenize)\
            .apply(lambda tokens: filter(not_stop, tokens))\
            .reset_index()
    
    cluster_corpus["keywords"] = cluster_corpus['doc'].apply(lambda x: cluster_keywords(x, tfidf_df))

    for index, cluster in cluster_corpus.iterrows():
        print(f"cluster {cluster['cluster']}")
        print(cluster["keywords"])


def sentiment_analysis(k, clusters_df, tfidf_df):

    find_keywords(clusters_df, tfidf_df)

#     clusters_df["sentiment_score"] = clusters_df["doc"].apply(sent_score)
    
#     sentiment_score_clusters = clusters_df.groupby("cluster").mean()["sentiment_score"]
#     print(sentiment_score_clusters)

    

#     for cluster_num in range(k):
#         cluster = clusters_df[clusters_df["cluster"] == cluster_num]
            
#         tfidf_df



def main():
    k = 3
    sentiment_analysis(k)
    k = 6
    sentiment_analysis(k)

if __name__ == "__main__":
    main()