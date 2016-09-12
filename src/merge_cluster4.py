import my_util


def get_list_threshold(threshold, max_threshold=1.0):
    list_thresholds = list()
    temp_threshold = max_threshold
    while temp_threshold >= threshold:
        list_thresholds.append(temp_threshold)
        temp_threshold = temp_threshold - 0.1
    list_thresholds = sorted(list_thresholds, reverse=True)
    return list_thresholds


def get_similarities_with_other_clusters(center_cluster, other_center_clusters):
    similarities = dict()
    for cluster_id in other_center_clusters.keys():
        other_center_cluster = other_center_clusters[cluster_id]
        similarity = my_util.get_similarity(center_cluster, other_center_cluster)
        similarities[cluster_id] = similarity
    return similarities


def merge_clusters_with_step_threshold(clusters, center_clusters, size_clusters, threshold_step):
    new_clusters = dict()
    new_center_clusters = dict()
    new_size_clusters = dict()
    dict_updated_cluster = dict()
    count = 0
    for cluster_id in clusters.keys():
        count += 1
        if count % 100 == 0:
            print count, '/', len(clusters)
        cluster = clusters[cluster_id]
        center_cluster = center_clusters[cluster_id]
        size_cluster = size_clusters[cluster_id]
        similarities = get_similarities_with_other_clusters(center_cluster, new_center_clusters)
        if len(similarities) > 0:
            max_cluster_id = my_util.get_key_max_value(similarities)
            max_similarity = similarities[max_cluster_id]
            if max_similarity >= threshold_step:
                # print 'Merge', cluster_id, 'into', max_cluster_id
                for vector_id in cluster:
                    new_clusters[max_cluster_id].append(vector_id)
                new_size_clusters[max_cluster_id] += len(cluster)
                dict_updated_cluster[max_cluster_id] = my_util.get_center_cluster2(new_center_clusters[max_cluster_id],
                                                                                   center_cluster,
                                                                                   new_size_clusters[max_cluster_id],
                                                                                   size_cluster)
            else:  # create new cluster
                # print 'Create new cluster', cluster_id
                new_clusters[cluster_id] = cluster
                new_size_clusters[cluster_id] = size_cluster
                new_center_clusters[cluster_id] = center_cluster
        else:
            # print 'Create new cluster', cluster_id
            new_clusters[cluster_id] = cluster
            new_size_clusters[cluster_id] = size_cluster
            new_center_clusters[cluster_id] = center_cluster

    # update center_cluster
    for max_cluster_id in dict_updated_cluster:
        new_center_clusters[max_cluster_id] = dict_updated_cluster[max_cluster_id]

    return (new_clusters, new_center_clusters, new_size_clusters)


def clustering_with_threshold(clusters, center_clusters, size_clusters, threshold, threshold_change_size=5):
    list_thresholds = get_list_threshold(threshold, max_threshold=0.7)
    print list_thresholds
    for threshold_step in list_thresholds:
        print '\nThreshold step =', threshold_step, '\n'
        while True:
            size_before_merge = len(clusters)
            (clusters, center_clusters, size_clusters) = merge_clusters_with_step_threshold(clusters, center_clusters,
                                                                                            size_clusters,
                                                                                            threshold_step)
            size_after_merge = len(clusters)
            decrease_cluster = size_before_merge - size_after_merge
            print 'decrease_cluster =', decrease_cluster
            if decrease_cluster < threshold_change_size:
                print 'Break: decrease <', threshold_change_size
                break

    return (clusters, center_clusters, size_clusters)
