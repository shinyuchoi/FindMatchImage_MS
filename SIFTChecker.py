import cv2
import numpy as np
import matplotlib.pyplot as plt


def imread_unicode(path, flags=cv2.IMREAD_COLOR):
    with open(path, 'rb') as f:
        data = np.asarray(bytearray(f.read()), dtype=np.uint8)
        img = cv2.imdecode(data, flags)
    return img

# === Load images ===
img1 = imread_unicode('C:\FindMatchImage_MS\git_Resources\limitSample01.png')  # 왼쪽 이미지
img2 = imread_unicode('images/와일드보어.jpg')  # 오른쪽 이미지

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# === SIFT detector ===
sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)

# === Feature matching (BF + Lowe's ratio test) ===
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)

# Apply ratio test
good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

# === Draw results ===
img_match = cv2.drawMatchesKnn(
    img1, kp1, img2, kp2, [[m] for m in good_matches],
    None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)

# === Show image ===
plt.figure(figsize=(14, 6))
plt.imshow(cv2.cvtColor(img_match, cv2.COLOR_BGR2RGB))
plt.title(f"Good Matches: {len(good_matches)}")
plt.axis("off")
plt.show()
