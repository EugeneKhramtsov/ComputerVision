import cv2
import numpy as np


def load_images(high_path, low_path):
    high_res = cv2.imread(high_path)
    low_res = cv2.imread(low_path)

    if high_res is None or low_res is None:
        raise ValueError("Images not found")

    return high_res, low_res


def preprocess(img):
    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=3.0,
        tileGridSize=(8, 8)
    )

    l2 = clahe.apply(l)

    merged = cv2.merge((l2, a, b))
    enhanced = cv2.cvtColor(
        merged,
        cv2.COLOR_LAB2BGR
    )

    return enhanced


def kmeans_segmentation(img, k=4):
    Z = img.reshape((-1, 3))
    Z = np.float32(Z)

    criteria = (
        cv2.TERM_CRITERIA_EPS +
        cv2.TERM_CRITERIA_MAX_ITER,
        10,
        1.0
    )

    _, label, center = cv2.kmeans(
        Z,
        k,
        None,
        criteria,
        10,
        cv2.KMEANS_RANDOM_CENTERS
    )

    center = np.uint8(center)

    result = center[label.flatten()]
    result = result.reshape(img.shape)

    labels = label.reshape(img.shape[:2])

    return result, labels


def extract_target_cluster(img, labels):
    cluster_means = []

    for i in range(np.max(labels) + 1):
        mask = labels == i
        mean = np.mean(img[mask])
        cluster_means.append(mean)

    target_cluster = np.argmax(cluster_means)

    mask = (
        (labels == target_cluster)
        .astype(np.uint8) * 255
    )

    return mask


def get_contours(mask):
    kernel = np.ones((5, 5), np.uint8)

    cleaned = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    contours, _ = cv2.findContours(
        cleaned,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    return contours, cleaned


def filter_circles(contours):
    circles = []

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < 100:
            continue

        perimeter = cv2.arcLength(contour, True)

        if perimeter == 0:
            continue

        circularity = (
            4 * np.pi *
            (area / (perimeter ** 2))
        )

        if 0.7 < circularity <= 1.2:
            circles.append(contour)

    return circles


def draw_circles(img, contours):
    result = img.copy()

    cv2.drawContours(
        result,
        contours,
        -1,
        (0, 255, 0),
        1
    )

    return result


def process_image(img):
    preprocessed = preprocess(img)

    kmeans_result, labels = kmeans_segmentation(
        preprocessed
    )

    mask = extract_target_cluster(
        kmeans_result,
        labels
    )

    contours, cleaned = get_contours(mask)

    circles = filter_circles(contours)

    result = draw_circles(img, circles)

    return {
        "preprocessed": preprocessed,
        "kmeans": kmeans_result,
        "labels": labels,
        "mask": mask,
        "cleaned": cleaned,
        "contours": contours,
        "circles": circles,
        "result": result
    }


def show_results(high_result, low_result):
    cv2.imshow("High-res", high_result)
    cv2.imshow("Low-res", low_result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    high_res, low_res = load_images(
        'images/high_res.jpg',
        'images/low_res.jpg'
    )

    high_data = process_image(high_res)
    low_data = process_image(low_res)

    print(
        "High-res objects found:",
        len(high_data["circles"])
    )

    print(
        "Low-res objects found:",
        len(low_data["circles"])
    )

    show_results(
        high_data["result"],
        low_data["result"]
    )


if __name__ == "__main__":
    main()