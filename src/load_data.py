# coding=utf-8
# load dictionary and news that saved in local folder ../data/
import parameter, my_util, merge_cluster1, merge_cluster2
import pickle
from gensim.corpora import Dictionary


def read_token_dictionary():
    token_dictionary = Dictionary.load_from_text('..' + parameter.FILE_DICTIONARY)
    return token_dictionary


def read_content():
    rb = open('..' + parameter.FILE_DATA, 'rb')
    data = pickle.load(rb)
    rb.close()
    return data


# get vector tf-idf of all news
def read_data():
    print 'Starting reload data from local folder ....'

    id_df_dict = dict()
    vectortfs = dict()

    token_dictionary = read_token_dictionary()
    token_id_dict = token_dictionary.token2id
    token_df_dict = token_dictionary.dfs
    for token in token_id_dict:
        id = token_id_dict[token]
        df = token_df_dict[id]
        id_df_dict[id] = df

    documents = read_content()
    count = 0
    for id_doc in documents:
        count += 1
        print count
        # if count > 1000:
        #     break
        document = documents[id_doc]
        vector = dict()
        for token in document:
            id = token_id_dict[token]
            if id in vector:
                vector[id] += 1
            else:
                vector[id] = 1
        vectortfs[id_doc] = vector

    print 'Done reload data!'
    print 'Starting get tfidf vectors ....'
    N = len(vectortfs)
    vectortfidfs = dict()
    for id_vector in vectortfs:
        vector = vectortfs[id_vector]
        vector = my_util.get_vector(vector, id_df_dict, N)
        vectortfidfs[id_vector] = vector

    print 'Done get tfidf vectors!'
    return vectortfidfs


def test_merge1():
    # read data
    vectortfidfs = read_data()
    center_clusters = dict()
    clusters = dict()
    for id_vector in vectortfidfs:
        vector = vectortfidfs[id_vector]
        cluster = dict()
        cluster[id_vector] = vector
        id_cluster = id_vector
        clusters[id_cluster] = cluster
        center_clusters[id_cluster] = vector

    threshold = 0.7
    print 'Before merge, size(clusters) =', len(clusters), 'size(center_clusters) =', len(center_clusters)
    merge_cluster1.merge_clusters_with_threshold(clusters, center_clusters, threshold)
    print 'After merge, size(clusters) =', len(clusters), 'size(center_clusters) =', len(center_clusters)

    for id_cluster in clusters:
        cluster = clusters[id_cluster]
        print cluster.keys()


def test_merge2():
    # read data
    vectortfidfs = read_data()  # vectors tfidf
    center_clusters = dict()  # center vectors of clusters
    clusters = dict()  # one cluster have many vector
    size_clusters = dict()
    for vector_id in vectortfidfs:
        vector = vectortfidfs[vector_id]
        cluster_id = vector_id
        center_clusters[cluster_id] = vector
        clusters[cluster_id] = [cluster_id]
        size_clusters[cluster_id] = 1

    threshold = 0.4
    print 'Before merge, size(clusters) =', len(clusters), 'size(center_clusters) =', len(center_clusters)
    merge_cluster2.merge_clusters_with_threshold(clusters, center_clusters, size_clusters, threshold)
    print 'After merge, size(clusters) =', len(clusters), 'size(center_clusters) =', len(center_clusters)

    print 'Tam oc cho'

    for cluster_id in clusters:
        cluster = clusters[cluster_id]
        print cluster


def main():
    test_merge2()


if __name__ == '__main__':
    main()
