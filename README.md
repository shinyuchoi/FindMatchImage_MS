# Real-Time Screen Image Matcher (SIFT-based)

This Python project performs real-time screen image matching using the SIFT feature detection algorithm. It extracts features from reference images, compares them with real-time screen captures, and displays the most similar matches in a visual overlay.

---

## Features

- Real-time screen capture & image similarity matching
- SIFT-based feature detection and matching
- Feature caching to `.npz` for performance
- GUI overlay to visualize capture region (Tkinter)
- Unicode path and Korean font support
- Multithreaded processing (UI + matching)

---

## Project Structure

```
project-root/
├── images/             # Input reference images (ignored in git)
├── savedData/          # Saved feature files (.npz) (ignored in git)
├── image_Processer.py  # Real-time feature matcher
├── preprocessing.py    # Feature extraction script
├── ui.py               # UI capture window overlay
└── main.py             # Entry point: initializes extraction + threads
```

---

## Requirements

- Python 3.8+
- OpenCV (`opencv-python`)
- Pillow
- pyautogui
- tqdm
- keyboard

### Install all dependencies:

```bash
pip install opencv-python pillow pyautogui tqdm keyboard
```

---

## How to Use

1. Add images  
   Put your reference `.jpg` / `.png` images into the `images/` folder.

2. Run the main script

```bash
python main.py
```

- If `savedData/` does not exist, or the number of `.npz` files doesn't match the number of images, feature extraction will run automatically.
- A semi-transparent red box will appear; move it over your screen to define the matching area.
- The script will display the top 7 matching images in a popup window.
- Press `Enter` key to exit.

---

## Logic Summary

- `main.py` handles initial checks and starts threads for:
  - `image_Processer.main_loop()` for continuous screen capture & matching
  - `UI.show_capture_window()` for visual capture overlay
- `preprocessing.py` extracts features using SIFT, ORB, BRISK, AKAZE (though only SIFT is used in matching).
- Matching is based on descriptor similarity using Lowe's ratio test.


## Future Improvements
- Combine results from multiple detectors (e.g., SIFT, ORB, AKAZE) to calculate an aggregated match score
  - Improve robustness by fusing results from different algorithms
- Improve matching accuracy using machine learning
  - Train a lightweight image classifier (e.g., MobileNet) to predict the best match
  - Combine SIFT-based ranking with model-based validation
- Enable user feedback loop to retrain with misclassified data
- Provide a simple web service (Flask or FastAPI) to expose the matching system
  - Upload screen captures and receive top-N matched images as response
  - 
---

## License

MIT License
