import my_util
import operator


def get_key_max_value(my_dict):
    return max(my_dict.iteritems(), key=operator.itemgetter(1))[0]


def merge_cluster2_into_cluster1(clusters, center_clusters, size_clusters, similarities, cluster_id1, cluster_id2):
    print 'Merge cluster (', cluster_id1, ',', cluster_id2, ')'
    cluster1 = clusters[cluster_id1]
    cluster2 = clusters[cluster_id2]
    for vector_id in cluster2:
        cluster1.append(vector_id)

    clusters[cluster_id1] = cluster1
    center_clusters[cluster_id1] = my_util.get_center_cluster2(center_clusters[cluster_id1],
                                                               center_clusters[cluster_id2],
                                                               size_clusters[cluster_id1], size_clusters[cluster_id2])

    del clusters[cluster_id2]
    del center_clusters[cluster_id2]
    del size_clusters[cluster_id2]

    # update similarities
    del similarities[(cluster_id1, cluster_id2)]
    for pair in similarities.keys():
        if cluster_id2 in pair:
            del similarities[pair]
        if cluster_id1 in pair:
            other_id = pair[0]
            if cluster_id1 == pair[0]:
                other_id = pair[1]
            my_util.get_simiarity(center_clusters[cluster_id1], center_clusters[other_id])


def merge_clusters_with_threshold(clusters, center_clusters, size_clusters, threshold):
    similarities = dict()
    cluster_ids = sorted(clusters.keys())
    N = len(cluster_ids)
    N = N * (N + 1) / 2
    count = 0
    print 'Building similarities ...'
    for index1 in range(0, len(cluster_ids) - 1):
        cluster_id1 = cluster_ids[index1]
        for index2 in range(index1 + 1, len(cluster_ids)):
            count += 1
            if count % 100000 == 0:
                print count, '/', N
            cluster_id2 = cluster_ids[index2]
            pair = (cluster_id1, cluster_id2)
            similarity = my_util.get_simiarity(center_clusters[cluster_id1], center_clusters[cluster_id2])
            similarities[pair] = similarity

    while True:
        pair = get_key_max_value(similarities)
        max_similarity = similarities[pair]
        print pair, '=', max_similarity
        if max_similarity < threshold:
            print 'Break while loop: max_similarity < threshold'
            break
        cluster_id1 = pair[0]
        cluster_id2 = pair[1]
        merge_cluster2_into_cluster1(clusters, center_clusters, size_clusters, similarities, cluster_id1, cluster_id2)


if __name__ == '__main__':
    my_dict = dict()
    my_dict[(1, 2)] = 2
    my_dict[(1, 3)] = 3
    my_dict[(1, 1)] = 1

    print my_dict
    print get_key_max_value(my_dict)
