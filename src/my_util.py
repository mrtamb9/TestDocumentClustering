# coding=utf-8

import math

VN_STR = ['_', u'a', u'b', u'c', u'd', u'e', u'f', u'g', u'h', u'i', u'j', u'k', u'l', u'm', u'n', u'o', u'p', u'q',
          u'r', u's', u't', u'u', u'v', u'w', u'x', u'y', u'z', u'á', u'à', u'ả', u'ã', u'ạ', u'ă', u'ắ', u'ặ', u'ằ',
          u'ẳ', u'ẵ', u'â', u'ấ', u'ầ', u'ẩ', u'ẫ', u'ậ', u'đ', u'é', u'è', u'ẻ', u'ẽ', u'ẹ', u'ê', u'ế', u'ề', u'ể',
          u'ễ', u'ệ', u'í', u'ì', u'ỉ', u'ĩ', u'ị', u'ó', u'ò', u'ỏ', u'õ', u'ọ', u'ô', u'ố', u'ồ', u'ổ', u'ỗ', u'ộ',
          u'ơ', u'ớ', u'ờ', u'ở', u'ỡ', u'ợ', u'ú', u'ù', u'ủ', u'ũ', u'ụ', u'ư', u'ứ', u'ừ', u'ử', u'ữ', u'ự', u'ý',
          u'ỳ', u'ỷ', u'ỹ', u'ỵ']


def check_valid_character(char):
    if char in VN_STR:
        return True
    return False


def check_valid_token(token):
    for index in range(len(token)):
        char = token[index]
        if not check_valid_character(char):
            return False
    return True


def get_vector(vector, id_df_dict, N):
    sqr_sum = 0
    for token_id in vector:
        tf = vector[token_id]
        df = id_df_dict[token_id]
        tfidf_value = (1 + math.log(tf)) * math.log(N * 1.0 / df)
        vector[token_id] = tfidf_value
        sqr_sum += tfidf_value * tfidf_value

    # normalize
    sqrt_sqr_sum = math.sqrt(sqr_sum)
    for token_id in vector:
        vector[token_id] = vector[token_id] * 1.0 / sqrt_sqr_sum

    return vector


def get_similarity(vector1, vector2):
    up = 0;
    down1 = 0
    down2 = 0
    for id1 in vector1:
        value1 = vector1[id1]
        down1 += value1 * value1
        if id1 in vector2:
            value2 = vector2[id1]
            up += value1 * value2

    for id2 in vector2:
        value2 = vector2[id2]
        down2 += value2 * value2

    down = down1 * down2
    if down > 0:
        down = math.sqrt(down)
        similarity = up / float(down)
        return similarity

    return 0


def get_center_cluster1(cluster):
    center_vector_of_cluster = dict()
    for id_vector in cluster:
        vector = cluster[id_vector]
        for token_id in vector:
            if token_id in center_vector_of_cluster:
                center_vector_of_cluster[token_id] += vector[token_id]
            else:
                center_vector_of_cluster[token_id] = vector[token_id]

    N = len(cluster)
    for token_id in center_vector_of_cluster:
        center_vector_of_cluster[token_id] = center_vector_of_cluster[token_id] * 1.0 / N

    return center_vector_of_cluster


def get_center_cluster2(center_vector1, center_vector2, size1, size2):
    center_vector_of_cluster = dict()
    for token_id1 in center_vector1:
        center_vector_of_cluster[token_id1] = 0
    for token_id2 in center_vector2:
        center_vector_of_cluster[token_id2] = 0

    for token_id in center_vector_of_cluster:
        value = 0
        if token_id in center_vector1:
            value += center_vector1[token_id] * size1
        if token_id in center_vector2:
            value += center_vector2[token_id] * size2
        center_vector_of_cluster[token_id] = value

    N = size1 + size2
    if N == 0:
        return None

    for token_id in center_vector_of_cluster:
        center_vector_of_cluster[token_id] = center_vector_of_cluster[token_id] / float(N)

    return center_vector_of_cluster

