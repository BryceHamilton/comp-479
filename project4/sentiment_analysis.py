import pandas as pd
from afinn import Afinn

afinn = Afinn()

def sent_score(df):
    return afinn.score(df)


def sentiment_analysis(k, clusters_df, tfidf_df):

    clusters_df["sentiment_score"] = clusters_df["doc"].apply(sent_score)

    sentiment_score_clusters = clusters_df.groupby("cluster").mean()["sentiment_score"]

    print(sentiment_score_clusters)

def main():
    for k in [3, 6]:
        clusters_df = pd.read_csv(f"clusters/{k}/clusters_df.csv")
        sentiment_analysis(k, clusters_df)

if __name__ == "__main__":
    main()