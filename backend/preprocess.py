import os
from PIL import Image, ImageOps
import cv2
import numpy as np

COLS = 13
ROWS = 2
CHARS = [chr(ord('a') + i) for i in range(26)]

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def crop_grid_and_clean(image_path, out_dir, margin=0.05):
    # image_path: scanned sheet
    # out_dir: folder where cleaned letter PNGs will be saved
    # margin: fraction inward from each cell to cut border whitespace
    ensure_dir(out_dir)
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    cell_w = w / COLS
    cell_h = h / ROWS

    for row in range(ROWS):
        for col in range(COLS):
            idx = row * COLS + col
            if idx >= 26:
                continue
            left = int(col * cell_w)
            upper = int(row * cell_h)
            right = int((col + 1) * cell_w)
            lower = int((row + 1) * cell_h)

            dx = int(cell_w * margin)
            dy = int(cell_h * margin)
            left += dx; upper += dy; right -= dx; lower -= dy

            crop = img.crop((left, upper, right, lower))
            cv_image = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2GRAY)
            cv_image = cv2.GaussianBlur(cv_image, (3,3), 0)
            th = cv2.adaptiveThreshold(cv_image, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)
            kernel = np.ones((2,2), np.uint8)
            th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)

            filename = os.path.join(out_dir, f"{CHARS[idx]}.png")
            cv2.imwrite(filename, th)
            print("Saved cleaned:", filename)
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python preprocess.py input_image out_dir")
        sys.exit(1)
    crop_grid_and_clean(sys.argv[1], sys.argv[2])