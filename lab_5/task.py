import cv2
import numpy as np

high_res = cv2.imread('images/high_res.jpg')
low_res = cv2.imread('images/low_res.jpg')

if high_res is None or low_res is None:
    raise ValueError('Images not found')

def preprocess(img):
    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l2 = clahe.apply(l)

    merged = cv2.merge((l2,a,b))
    enhanced = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    return enhanced

high_res_prep = preprocess(high_res)
low_res_prep = low_res

def kmeans_segmentation(img, k = 4):
    Z = img.reshape((-1, 3))
    Z = np.float32(Z)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, label, center = cv2.kmeans(Z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape((img.shape))

    return result, label.reshape(img.shape[:2])

high_kmeans, high_labels = kmeans_segmentation(high_res_prep)
low_kmeans, low_labels = kmeans_segmentation(low_res_prep)

def extract_target_cluster(img, labels):
    cluster_means = []
    for i in range(np.max(labels) + 1):
        mask = labels == i
        mean = np.mean(img[mask])
        cluster_means.append(mean)

    target_cluster = np.argmax(cluster_means)

    mask = (labels == target_cluster).astype(np.uint8) * 255

    return mask

high_mask = extract_target_cluster(high_kmeans, high_labels)
low_mask = extract_target_cluster(low_kmeans, low_labels)

def get_contours(mask):
    kernel = np.ones((5, 5), np.uint8)
    cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours, cleaned

high_contours, high_clean = get_contours(high_mask)
low_contours, low_clean = get_contours(low_mask)

def filter_circles(contours):
    circles = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 100:
            continue
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue

        circularity = 4 * np.pi * (area / (perimeter ** 2))

        if 0.7 < circularity <= 1.2:
            circles.append(contour)

    return circles

high_circles = filter_circles(high_contours)
low_circles = filter_circles(low_contours)

def draw_circles(img, contours):
    result = img.copy()
    cv2.drawContours(result, contours, -1, (0, 255, 0), 1)
    return result

high_result = draw_circles(high_res, high_circles)
low_result = draw_circles(low_res, low_circles)

print("High-res objects found: ", len(high_circles))
print("Low-res objects found: ", len(low_circles))

cv2.imshow("High-res", high_res_prep)
cv2.imshow("Low-res", low_res_prep)
cv2.waitKey(0)
cv2.imshow("High-res", high_kmeans)
cv2.imshow("Low-res", low_kmeans)
cv2.waitKey(0)
cv2.imshow("High-res", high_mask)
cv2.imshow("Low-res", low_mask)
cv2.waitKey(0)
cv2.imshow("High-res", high_clean)
cv2.imshow("Low-res", low_clean)
cv2.waitKey(0)
cv2.imshow("High-res", high_result)
cv2.imshow("Low-res", low_result)
cv2.waitKey(0)
cv2.destroyAllWindows()
