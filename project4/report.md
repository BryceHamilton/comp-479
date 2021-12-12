# COMP 479 - Project 4

### Bryce Hamilton - Fall 2021

## Crawler

In order to accumulate html documents for processes, the crawler extends `scrapy.Spider`. This library was ready out of the box, compared to other libraries like `spidy` that required additional maintenance to get up and running.

After creating a full `scrapy` project with `scrapy createproject`, it was discover that `scrapy` provided a much more lightweight way of integrated their functionality, through merely importing the `scrapy.Spider`, extending and implementing its methods.

The library is well documented, and was clear about how to initialize the class with a `name`, `start_url` (Concordia.ca), and `custom_settings` in order to obey `robots.txt`. There relveant examples on how to implement its `Spider.parse` method, in order to parse the response of a given url request, and follow all `<a>` (anchor, external link) tags using `response.follow` to continue crawling.

It was chosen to directly parse and save then `html` reponse, rather than merely accumulate `urls` to be parsed later, taking a single pass through the websites and responses rather than two.

`scrapy` also provived both the command line entry point for starting a crawler, and also a called Python API. The latter was used, and implements a `limit` parameter that sets an upper bound for the number of `html` files that may be downloaded from the crawling. The default value for this limit is `100`, in the interest of time, however, higher limits such as `300` or `1000` will produce more interesting results as the crawler has the opportunity to reach a diversity of websites, and therefore result in more distinct clustering and keywords.

Features:

- Accepts upper bound on downloaded files
- Obeys `robots.txt`
- `html` files saved to `/docs_html` under webpage title

## Extractor

Reads from `/docs_html` directly and creates a document stream, similar to previous projets, by `yield`ing a `doc_title, file_content` for every document found in the `/docs_html` directory, read in by the built-in python operating system and file-reading libraries.

Using this document stream generator, each document is parsed using `BeautifulSoup` with the `'html.parser'` option. `BeautifulSoup` provides a very good API for interacting with many different selections of a parsed document, however, all that is need in this case is the `get_text()` method to retrieve all text from the `html` document.

After parsing and extracting text, some cleaning and normalization is required, removing extra whitespace throughout the document text with regex `re.sub(' +')`, remove new lines, and case folding to normalize tokens in each document.

Finally, the text extracted from each document and cleaned is saved into the `/docs_txt` directory, under the same title.

## Clustering

Building on the previous steps of the pipeline, the `cluster` module reads the texts files that were extracted and saved in the previous step, from `/docs_txt`.

Reading these text files outputs two lists, to be used as `pandas.Series` i.e columns of tabular data. This modules and the subsequent modules use a `pandas` to manage the represenation of the clusters as tabular data, this faciliates actions based on cluster, i.e. `groupby` cluster.

After reading the text files, a term frequency, inverse document frequency table is created, storing the `tfidf` of each term, using the `sklearn` `TfidfVectorizer` module. TFIDF is a standard measure of the informativeness of a given term and will be used to compile keywords of clusters. The `TfidfVectorizer` module is used again to vectorize the documents for kmeans clustering. The `tfidf` table is returned as a `pandas.Dataframe`.

The main clustering step involves vectorizing all documents using `TfidfVectorizer` using `english` stop words, followed by employing the `sklearn` `KMeans` module. The initialization used is `k-means++` as it will produce more distinct clusters and a better run time, given the initial centroids are more likely to be an even distance apart. The other hyperparameters are roughly the default of sklearn, and increaseing the the max iterations or total runs did not produce substantial results but took natrually took longer.

The output of each clustering run, `3` and `6` clusters, are saved as `pandas.Dataframes` to their respective subdirectories in the `clusters` directory as well as the `titles` of documents of each cluster.

- Resources: https://towardsdatascience.com/clustering-documents-with-python-97314ad6a78d

## Keywords

Reading in the `tfidf` data on terms generated from the pre-clustering step, the `keywords` module iterates for each set of clusters, `3` and `6`, and finds the keywords for each cluster for each set.

The keywords are chosen by first joining all documents in a given cluster into a single document, tokenizing the document, and filtering out stop words.

```python
cluster_corpus = df.groupby("cluster")["doc"]\
        .apply(' '.join)\
        .apply(word_tokenize)\
        .apply(lambda tokens: filter(not_stop, tokens))\
        .reset_index()
```

These terms for each cluster are then cherry picked from the `tdidf` term data, and returning in descending order, with a limit of 50 as the `top 50 keywords`. An improvement on this would be to consider the "cluster term frequency" of each term, as they seem to be just the `idf` of each term that occurs in a given cluster, these terms have equal `tfidf` across clusters, which is not representative. Another algorithm considered for choosing keywords was `TextRank`, but `tfidf` was much more accesible with the prexisting infrastructure.

Aside from the keywords, a `wordcloud` is generated for each cluster. Both the `keywords` and `wordcloud` for each cluster is saved in the respective subdirectory of the `clusters` directory.

## Sentiment Analysis

Finally, after clustering and keywords have been generated, the cluster sets of `k = 3` and `k = 6` are read into the `sentiment_analysis` module. Using `pandas` the documents are grouped by cluster, and a sentintment score for each cluster is calculated by taking the mean average of the sentiment score output of each document in the cluster output by the `Afinn.score` third party library module.

The output of each cluster is saved to the `{cluster_num}_sentiment_score.txt` of each cluster's subdirectory. Generally sentiment scores are higher for concordia related documents that contain positive encouragement and mental health resource links, lower for things like STM customer service, and in the middle for youtube content/admin sites.

## Output

The standard output of a clustering pipeline run is visible in the `demo.txt` file, and the saved output of the clusters is visible in the `/saved_clusters` directory.
