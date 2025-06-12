import cv2
import numpy as np
import matplotlib.pyplot as plt

def imread_unicode(path, flags=cv2.IMREAD_COLOR):
    with open(path, 'rb') as f:
        data = np.asarray(bytearray(f.read()), dtype=np.uint8)
        img = cv2.imdecode(data, flags)
    return img

# === Keypoint visualization ===
img = imread_unicode('images/와일드보어.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(gray, None)

img_with_kp = cv2.drawKeypoints(img, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

plt.imshow(cv2.cvtColor(img_with_kp, cv2.COLOR_BGR2RGB))
plt.title(f"Keypoints: {len(keypoints)}")
plt.axis('off')
plt.show()

# === Match visualization ===
img1 = imread_unicode('git_Resources/limitation/limitationBoar.png')
img2 = imread_unicode('images/노마.jpg')

if img1 is None or img2 is None:
    print("[ERROR] One of the images failed to load.")
    exit()

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)

good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

img_match = cv2.drawMatchesKnn(
    img1, kp1, img2, kp2, [[m] for m in good_matches],
    None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)

plt.figure(figsize=(14, 6))
plt.imshow(cv2.cvtColor(img_match, cv2.COLOR_BGR2RGB))
plt.title(f"Good Matches: {len(good_matches)}")
plt.axis("off")
plt.show()
