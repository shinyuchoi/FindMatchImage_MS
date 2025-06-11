import cv2
import numpy as np
import os
import pyautogui
import threading
import time
from PIL import Image, ImageDraw, ImageFont

detector_name = 'SIFT'  # Feature detector name
detector = cv2.SIFT_create(nfeatures=5000)  # Initialize SIFT detector

# Read image with Unicode (e.g., Korean) file path support
def imread_unicode(filename, flags=cv2.IMREAD_COLOR):
    with open(filename, 'rb') as f:
        data = np.asarray(bytearray(f.read()), dtype=np.uint8)
    img = cv2.imdecode(data, flags)
    return img


# Draw Unicode text (e.g., Korean) on image using PIL
# Includes text border for better readability
def draw_text_unicode(img, text, position, font_size=20, text_color=(255, 255, 0), border_color=(0, 0, 0)):
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    font_path = "C:/Windows/Fonts/malgunbd.ttf"  # Windows Korean font
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img_pil)
    x, y = position

    # Draw border by shifting text in 8 directions
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=border_color)
    draw.text((x, y), text, font=font, fill=text_color)

    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


# Compute matching score using Lowe's ratio test
def compute_match_score(des1, des2, ratio_thresh=0.75):
    if des1 is None or des2 is None:
        return 0
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good = [m for m, n in matches if m.distance < ratio_thresh * n.distance]
    return len(good)


# Capture a region of the screen using pyautogui
def capture_screen(region):
    screenshot = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


# Find the top N matching images from the database
# Based on SIFT feature matching

def find_top_matches(input_img, top_n, feature_folder='savedData', image_folder='images'):
    input_gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    kp_input, des_input = detector.detectAndCompute(input_gray, None)

    if des_input is None:
        print("[ERROR] No descriptors found in captured image!")
        return

    match_scores = []
    feature_files = [f for f in os.listdir(feature_folder) if f.endswith('.npz')]

    for ffile in feature_files:
        try:
            data = np.load(os.path.join(feature_folder, ffile), allow_pickle=True)
            des_db_key = detector_name + '_descriptors'
            if des_db_key not in data:
                continue

            des_db = data[des_db_key]
            # Skip if dimensions mismatch
            if des_db is None or des_db.ndim != 2 or des_input.shape[1] != des_db.shape[1]:
                continue

            score = compute_match_score(des_input, des_db)
            match_scores.append((ffile, score))
        except Exception as e:
            print(f"[ERROR] Failed to process {ffile}: {e}")
            continue

    match_scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score descending
    top_matches = match_scores[:top_n]

    matched_images = []
    for filename, score in top_matches:
        base_filename = filename.replace('.npz', '')
        matched_img_path = os.path.join(image_folder, base_filename)

        if os.path.exists(matched_img_path):
            matched_img = imread_unicode(matched_img_path)
            if matched_img is not None:
                matched_img = cv2.resize(matched_img, (200, 200))
                filename_only = os.path.splitext(os.path.basename(base_filename))[0]
                matched_img = draw_text_unicode(matched_img, filename_only, (5, 170), font_size=20)
                matched_images.append(matched_img)

    # Show concatenated matching results
    if matched_images:
        collage = np.hstack(matched_images)
        cv2.imshow(f"Top Matches ({threading.current_thread().name})", collage)
        cv2.waitKey(1)


# Main processing loop
# Periodically captures screen and finds top matching images
def main_loop(region, top_n=7, rate=0.5):
    while True:
        input_img = capture_screen(region)
        find_top_matches(input_img, top_n)
        time.sleep(rate)