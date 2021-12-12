import pandas as pd
from afinn import Afinn

afinn = Afinn()


def sentiment_analysis(k, clusters_df):

    clusters_df["sentiment_score"] = clusters_df["doc"].apply(afinn.score)

    sentiment_score_clusters = clusters_df.groupby("cluster").mean()["sentiment_score"]

    print(sentiment_score_clusters)

    for cluster_num, score in sentiment_score_clusters.items():
        with open(f"clusters/{k}/{cluster_num}/{cluster_num}_sentiment_score.txt", 'w') as f:
                f.write(str(score))

def main():
    for k in [3, 6]:
        clusters_df = pd.read_csv(f"clusters/{k}/clusters_df.csv")
        sentiment_analysis(k, clusters_df)

if __name__ == "__main__":
    main()