import keyboard
import preProcessing
import threading
import time
import image_Processer
import UI
import os

# === Configuration ===
top_n = 5
rate = 0.5
image_folder = 'images'
feature_folder = 'savedData'

print("**** Start ****")

# === Conditional feature extraction ===
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Check if feature folder exists
if not os.path.exists(feature_folder):
    print(f"[INFO] Feature folder '{feature_folder}' not found. Creating and extracting features...")
    preProcessing.extract_features(image_folder, feature_folder)
    print("Feature extraction completed!")
else:
    feature_files = [f for f in os.listdir(feature_folder) if f.endswith('.npz')]

    if len(image_files) != len(feature_files):
        print(f"[INFO] Mismatch: {len(image_files)} images, {len(feature_files)} features. Re-extracting...")
        preProcessing.extract_features(image_folder, feature_folder)
        print("Feature extraction completed!")
    else:
        print("Feature data is up-to-date. Skipping extraction.")

# === Define capture region (x, y, width, height) ===
region1 = [900, 500, 170, 170]

if __name__ == "__main__":
    # Start image matching thread
    threading.Thread(
        target=image_Processer.main_loop,
        args=(region1, top_n, rate),
        daemon=True
    ).start()

    # Start UI overlay thread
    threading.Thread(
        target=UI.show_capture_window,
        args=(region1,),
        daemon=True
    ).start()

    # Wait for Enter key to exit
    while True:
        if keyboard.is_pressed("enter"):
            print("Exit Program")
            break
        time.sleep(0.1)