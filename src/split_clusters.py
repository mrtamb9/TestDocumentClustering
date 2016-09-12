import my_util


# get corehence of cluster
def get_coherence_of_cluster(cluster, center_cluster, vectortfidfds):
    coherence = 0
    for vector_id in cluster:
        vector = vectortfidfds[vector_id]
        similarity = my_util.get_similarity(vector, center_cluster)
        coherence += similarity

    if coherence == 0:
        print "Error: "
        print cluster
        print center_cluster
        exit()
        return 0

    coherence = coherence / float(len(cluster))
    return coherence


# kiem tra chat luong cum:
# - do khoang cach tu cac vector den center_cluster
def check_quality_cluster(cluster, center_cluster, vectortfidfs, threshold_quality):
    coherence = get_coherence_of_cluster(cluster, center_cluster, vectortfidfs)
    if coherence < threshold_quality:
        return False
    return True


# tach 1 cluster thanh 2 clusters con:
# - tim ra 2 vector xa nhau nhat, sau do tach thanh 2 cluster, moi cluster chua 1 trong 2 vector nay
def split_cluster(cluster, vectortfidfs):
    # get pair vectors that min similarity
    min_similarity = 1000
    min_pair = None
    vector_ids = sorted(cluster)
    for index1 in range(0, len(vector_ids) - 1):
        vector_id1 = vector_ids[index1]
        vector1 = vectortfidfs[vector_id1]
        for index2 in range(index1 + 1, len(vector_ids)):
            vector_id2 = vector_ids[index2]
            vector2 = vectortfidfs[vector_id2]
            similarity = my_util.get_similarity(vector1, vector2)
            if similarity < min_similarity:
                min_similarity = similarity
                min_pair = (vector_id1, vector_id2)

    print 'Min pair =', min_pair
    # split cluster into 2 clusters
    vector_id1 = min_pair[0]
    vector_id2 = min_pair[1]
    vector1 = vectortfidfs[vector_id1]
    vector2 = vectortfidfs[vector_id2]
    cluster1 = list([vector_id1])
    cluster2 = list([vector_id2])
    for vector_id in cluster:
        if vector_id != vector_id1 and vector_id != vector_id2:
            vector = vectortfidfs[vector_id]
            similarity1 = my_util.get_similarity(vector, vector1)
            similarity2 = my_util.get_similarity(vector, vector2)
            if similarity1 >= similarity2:
                cluster1.append(vector_id)
            else:
                cluster2.append(vector_id)

    return (cluster1, cluster2)
