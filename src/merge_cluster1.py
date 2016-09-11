import my_util


def get_pair_cluster_max_similarity(dict_similarity):
    max_simiarity = 0
    pair_cluster = ''
    for key in dict_similarity:
        similarity = dict_similarity[key]
        if similarity > max_simiarity:
            max_simiarity = similarity
            pair_cluster = key
            if max_simiarity == 1.0:
                break

    cluster_id1 = int(pair_cluster.split('_')[0])
    cluster_id2 = int(pair_cluster.split('_')[1])
    return (cluster_id1, cluster_id2, max_simiarity)


def merge_2_clusters_into_1(clusters, center_clusters, dict_similarity, cluster_id1, cluster_id2):
    print 'Merge', cluster_id1, 'into', cluster_id2
    cluster1 = clusters[cluster_id1]
    cluster2 = clusters[cluster_id2]

    del clusters[cluster_id1]
    del center_clusters[cluster_id1]

    for id_vector in cluster1:
        vector = cluster1[id_vector]
        cluster2[id_vector] = vector

    clusters[cluster_id2] = cluster2
    center_clusters[cluster_id2] = my_util.get_center_cluster1(cluster2)

    # remove from dict_similarity
    list_del_key = dict_similarity.keys()
    for cluster_id in list_del_key:
        if (str(cluster_id1) in cluster_id.split('_')) or (str(cluster_id2) in cluster_id.split('_')):
            del dict_similarity[cluster_id]

    # calculate similarity from new cluster with other clusters
    for cluster_id in center_clusters:
        if cluster_id != cluster_id2:
            similarity = my_util.get_simiarity(center_clusters[cluster_id2], center_clusters[cluster_id])
            add_element_into_dict_similarity(dict_similarity, cluster_id, cluster_id2, similarity)


def add_element_into_dict_similarity(dict_similarity, id1, id2, similarity):
    key = ''
    if id1 < id2:
        key = str(id1) + '_' + str(id2)
    else:
        key = str(id2) + '_' + str(id1)
    dict_similarity[key] = similarity


def merge_clusters_with_threshold(clusters, center_clusters, threshold):
    dict_similarity = dict()
    count = 0
    for cluster_id1 in center_clusters:
        vector1 = center_clusters[cluster_id1]
        count += 1
        print count
        for cluster_id2 in center_clusters:
            if cluster_id2 != cluster_id1:
                vector2 = center_clusters[cluster_id2]
                simiarity = my_util.get_simiarity(vector1, vector2)
                add_element_into_dict_similarity(dict_similarity, cluster_id1, cluster_id2, simiarity)

    (cluster_id1, cluster_id2, max_simiarity) = get_pair_cluster_max_similarity(dict_similarity)
    print 'max_simiarity =', max_simiarity
    while max_simiarity >= threshold:
        print 'Cluster.size() =', len(clusters)
        merge_2_clusters_into_1(clusters, center_clusters, dict_similarity, cluster_id1, cluster_id2)
        (cluster_id1, cluster_id2, max_simiarity) = get_pair_cluster_max_similarity(dict_similarity)
        print 'max_simiarity =', max_simiarity
