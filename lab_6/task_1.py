import cv2 as cv
from lab_5.task import preprocess
from lab_5.task import kmeans_segmentation
from lab_5.task import extract_target_cluster
from lab_5.task import get_contours

def SIFT_Feature_Matching(filename_1, filename_2):
    img1, img2 = prepare_images(filename_1, filename_2)

    sift = cv.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    matchesMask = [[0, 0] for i in range(len(matches))]

    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matchesMask[i] = [1, 0]

    draw_params = dict(matchColor = (0, 255, 0),
                       singlePointColor = (255, 0, 0),
                       matchesMask = matchesMask,
                       flags = cv.DrawMatchesFlags_DEFAULT)

    img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)

    cv.imshow('SIFT_Feature_Matching', img3)
    cv.waitKey(0)

    return

def prepare_images(filename_1, filename_2):
    high_res = cv.imread(filename_1)
    low_res = cv.imread(filename_2)
    high_res_prep = preprocess(high_res)
    low_res_prep = low_res
    high_kmeans, high_labels = kmeans_segmentation(high_res_prep)
    low_kmeans, low_labels = kmeans_segmentation(low_res_prep)
    high_mask = extract_target_cluster(high_kmeans, high_labels)
    low_mask = extract_target_cluster(low_kmeans, low_labels)
    _, high_clean = get_contours(high_mask)
    _, low_clean = get_contours(low_mask)
    cv.waitKey(0)

    return high_mask, low_mask

SIFT_Feature_Matching('images/high_res.jpg', 'images/low_res.jpg')
