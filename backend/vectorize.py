import os
import subprocess
import cv2

def png_to_pbm(png_path, pbm_path):
    img = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"File not found: {png_path}")
    _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    img_bin = 255 - img_bin
    cv2.imwrite(pbm_path, img_bin)

def vectorize_with_potrace(pbm_path, out_svg_path):
    cmd = ['potrace', pbm_path, '-s', '-o', out_svg_path]
    subprocess.check_call(cmd)

def batch_vectorize(png_dir, svg_out_dir):
    os.makedirs(svg_out_dir, exist_ok=True)
    for filename in sorted(os.listdir(png_dir)):
        if not filename.lower().endswith('.png'):
            continue
        name = os.path.splitext(filename)[0]
        png_path = os.path.join(png_dir, filename)
        pbm_path = os.path.join(svg_out_dir, name + '.pbm')
        svg_path = os.path.join(svg_out_dir, name + '.svg')
        print("Converting", png_path, "->", svg_path)
        png_to_pbm(png_path, pbm_path)
        vectorize_with_potrace(pbm_path, svg_path)
        try:
            os.remove(pbm_path)
        except:
            pass
    print("Vectorization done.")
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python vectorize.py png_dir svg_out_dir")
        sys.exit(1)
    batch_vectorize(sys.argv[1], sys.argv[2])
