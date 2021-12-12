import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk import word_tokenize
from nltk.corpus import stopwords

stop_words = stopwords.words('english')


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

        with open(f"clusters/{k}/{cluster_num}/{cluster_num}_titles.txt", 'w') as f:
                f.write(titles.to_string(index=False))
        
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

        wordcloud.to_file(f"clusters/{k}/{cluster_num}/{cluster_num}_cloud.png")

def cluster_keywords(cluster_doc, tfidf_df):
    cluster_tfidf = tfidf_df[tfidf_df['term'].isin(cluster_doc)]
    cluster_tfidf = cluster_tfidf.sort_values('TF-IDF', ascending=False)
    print(cluster_tfidf.head(5))
    return cluster_tfidf['term'].head(50).tolist()

def not_stop(token):
    return token not in stop_words

def find_keywords(k, df, tfidf_df):

    cluster_corpus = df.groupby("cluster")["doc"]\
            .apply(' '.join)\
            .apply(word_tokenize)\
            .apply(lambda tokens: filter(not_stop, tokens))\
            .reset_index()
    
    cluster_corpus["keywords"] = cluster_corpus['doc'].apply(lambda x: cluster_keywords(x, tfidf_df))

    for index, cluster in cluster_corpus.iterrows():
        cluster_num = cluster['cluster']
        
        print(f"cluster {cluster_num}")
        print(cluster["keywords"])
        
        with open(f"clusters/{k}/{cluster_num}/{cluster_num}_keywords.txt", 'w') as f:
                for keyword in cluster["keywords"]:
                        f.write(keyword)
                        f.write("\n")

def main():
    tfidf_df = pd.read_csv(f"tf_idf.csv")
    for k in [3, 6]:
        clusters_df = pd.read_csv(f"clusters/{k}/clusters_df.csv")
        find_keywords(k, clusters_df, tfidf_df)
        print_clusters(k, clusters_df)

if __name__ == '__main__':
    main()