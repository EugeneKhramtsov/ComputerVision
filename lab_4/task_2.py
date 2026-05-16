import cv2

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("Edges", cv2.WINDOW_NORMAL)

cv2.resizeWindow("Frame", 1280, 720)
cv2.resizeWindow("Edges", 1280, 720)

input_file = "video.mp4"
cap = cv2.VideoCapture(input_file)

template = cv2.imread("template.jpg", 0)

template = cv2.GaussianBlur(template, (5, 5), 0)

_, template_bin = cv2.threshold(template, 135, 255, cv2.THRESH_BINARY)

contours_template, _ = cv2.findContours(template_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

template_contour = max(contours_template, key=cv2.contourArea)

perimetr_template = cv2.arcLength(template_contour, True)

approx_template = cv2.approxPolyDP(template_contour, 0.02 * perimetr_template, True)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    l = clahe.apply(l)

    lab = cv2.merge((l, a, b))

    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    blurred = cv2.GaussianBlur(enhanced, (9, 9), 0)

    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    gray = cv2.equalizeHist(gray)

    edges = cv2.Canny(gray, 150, 450)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < 100:
            continue
        perimetr = cv2.arcLength(contour, True)

        approx = cv2.approxPolyDP(contour, 0.02 * perimetr, True)

        similarity = cv2.matchShapes(approx_template, approx, 1, 0.0)
        similarity_str = str(round(similarity))
        if similarity >= 14 and similarity <= 18:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.putText(frame, similarity_str, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Edges", edges)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()

cv2.destroyAllWindows()