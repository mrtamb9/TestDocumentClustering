import my_util


def get_list_threshold(threshold, max_threshold=1.0):
    list_thresholds = list()
    temp_threshold = max_threshold
    while temp_threshold >= threshold:
        list_thresholds.append(temp_threshold)
        temp_threshold = temp_threshold - 0.05
    list_thresholds = sorted(list_thresholds, reverse=True)
    return list_thresholds


def merge_cluster2_into_cluster1(clusters, center_clusters, size_clusters, cluster_id1, cluster_id2):
    print 'Merge cluster', cluster_id2, 'into', cluster_id1
    cluster1 = clusters[cluster_id1]
    cluster2 = clusters[cluster_id2]
    for vector_id in cluster2:
        cluster1.append(vector_id)
    clusters[cluster_id1] = cluster1
    center_clusters[cluster_id1] = my_util.get_center_cluster2(center_clusters[cluster_id1],
                                                               center_clusters[cluster_id2],
                                                               size_clusters[cluster_id1],
                                                               size_clusters[cluster_id2])
    size_clusters[cluster_id1] = size_clusters[cluster_id1] + size_clusters[cluster_id2]

    del clusters[cluster_id2]
    del center_clusters[cluster_id2]
    del size_clusters[cluster_id2]


def merge_clusters_gte_threshold(clusters, center_clusters, size_clusters, similarities, my_threshold):
    list_pair_candidates = list()
    for pair in similarities.keys():
        if similarities[pair] >= my_threshold:
            list_pair_candidates.append(pair)

    for pair in list_pair_candidates:
        if pair[0] in clusters.keys() and pair[1] in clusters.keys():
            merge_cluster2_into_cluster1(clusters, center_clusters, size_clusters, pair[0], pair[1])


def merge_clusters_with_threshold(clusters, center_clusters, size_clusters, threshold):
    # build list pair similarities
    print 'Starting build list pair similarities ....'
    similarities = dict()
    for cluster_id1 in clusters:
        for cluster_id2 in clusters:
            if cluster_id1 < cluster_id2:
                pair_clusters = (cluster_id1, cluster_id2)
                similarity = my_util.get_simiarity(center_clusters[cluster_id1], center_clusters[cluster_id2])
                similarities[pair_clusters] = similarity

    list_thresholds = get_list_threshold(threshold, 1.0)
    for my_threshold in list_thresholds:
        while True:
            print 'My threshold =', my_threshold
            clusters_size_before = len(clusters)
            merge_clusters_gte_threshold(clusters, center_clusters, size_clusters, similarities, my_threshold)
            clusters_size_after = len(clusters)
            print 'Clusters size after merge =', len(clusters)
            print 'tam oc cho'
            decrease = clusters_size_before - clusters_size_after
            if decrease == 0:
                break
