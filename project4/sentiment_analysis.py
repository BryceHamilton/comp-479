import pandas as pd
from afinn import Afinn

afinn = Afinn()

def sent_score(df):
    return afinn.score(df)

def find_keywords(df):
    print("printing cluster words")
    print(df.groupby("cluster")["doc"]\
            .apply(' '.join)\
            .apply(lambda x: x.split(" "))\
            .apply(set)\
            .apply(list)\
            .reset_index())
    


def sentiment_analysis(k, clusters_df, tfidf_df):

    find_keywords(clusters_df)

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