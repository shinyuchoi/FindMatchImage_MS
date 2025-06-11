import cv2
import os
import numpy as np
from tqdm import tqdm

'''
This script loads images from the 'images' directory and extracts feature data (SIFT, ORB, BRISK, AKAZE),
then saves the keypoints and descriptors into the 'savedData' folder as .npz files.
'''

###
def extract_features(image_folder='images', feature_folder='savedData'):
    # Create output folder if it doesn't exist
    os.makedirs(feature_folder, exist_ok=True)

    # Initialize multiple feature detectors
    detector_dict = {
        'SIFT': cv2.SIFT_create(),
        'ORB': cv2.ORB_create(),
        'BRISK': cv2.BRISK_create(),
        'AKAZE': cv2.AKAZE_create()
    }

    # Convert keypoints to numpy array format
    def keypoints_to_array(keypoints):
        return np.array([
            [kp.pt[0], kp.pt[1], kp.size, kp.angle, kp.response, kp.octave, kp.class_id]
            for kp in keypoints
        ])

    # Read image with Unicode (e.g., Korean) path support
    def imread_unicode(filename, flags=cv2.IMREAD_COLOR):
        with open(filename, 'rb') as f:
            data = np.asarray(bytearray(f.read()), dtype=np.uint8)
        img = cv2.imdecode(data, flags)
        return img

    # List all image files in the folder
    image_files = [f for f in os.listdir(image_folder)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Process each image and extract features
    for img_file in tqdm(image_files, desc="Extracting features"):
        img_path = os.path.join(image_folder, img_file)

        # Load image in grayscale
        img = imread_unicode(img_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            print(f"[WARN] Failed to load image: {img_path}")
            continue

        feature_data = {}

        # Apply each detector and store results
        for name, detector in detector_dict.items():
            kp, des = detector.detectAndCompute(img, None)
            if des is not None and len(kp) > 0:
                feature_data[name + '_keypoints'] = keypoints_to_array(kp)
                feature_data[name + '_descriptors'] = des

        # Save extracted features to .npz file
        if feature_data:
            save_path = os.path.join(feature_folder, img_file + '.npz')
            np.savez_compressed(save_path, **feature_data)
        else:
            print(f"[WARN] Feature extraction failed: {img_path}")
