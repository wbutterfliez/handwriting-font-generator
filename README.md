# ✍️ H2F — Handwriting to Font

**H2F (Handwriting to Font)** is a tool that converts handwritten characters into a fully usable digital font.
Users can upload a handwriting sample through a simple web interface, preview the generated characters, rename the font, and download the final **.ttf font file**.

The system combines **computer vision, vector tracing, and font generation** to transform handwriting into a digital typeface.

---

## ✨ Features

* ✍️ Upload handwritten character sheets through a **web UI**
* 🔎 Automatic **character extraction and processing**
* 🧠 Computer vision powered preprocessing using **OpenCV**
* 🧾 Bitmap to vector conversion with **Potrace**
* 🔤 Automatic glyph mapping using **FontForge**
* 👀 **Live preview** of generated characters
* 📝 Rename the font before export
* 📦 Download a ready-to-use **TrueType (.ttf) font**

---

## 🛠 Tech Stack

**Languages**

* Python
* HTML / CSS / JavaScript

**Libraries & Tools**

* OpenCV — image preprocessing and character segmentation
* NumPy — numerical operations
* Pillow — image processing
* Potrace — bitmap to vector conversion
* FontForge — glyph creation and font generation

---

## ⚙️ How It Works

The system follows a processing pipeline to transform handwriting into a digital font.

```
Handwriting Upload (UI)
        ↓
Image Preprocessing (OpenCV)
        ↓
Character Segmentation
        ↓
Bitmap → Vector Conversion (Potrace)
        ↓
Glyph Mapping (FontForge)
        ↓
Font Generation (.ttf)
        ↓
Live Preview + Download
```

### 1. Upload Handwriting

Users upload a handwriting sample through the web interface.

### 2. Image Processing

The image is cleaned and prepared using **OpenCV** techniques such as:

* Grayscale conversion
* Thresholding
* Noise removal
* Contour detection

### 3. Character Extraction

Individual characters are segmented from the image.

### 4. Vector Conversion

Each character bitmap is converted into **vector paths** using **Potrace**.

### 5. Font Creation

Vector glyphs are mapped to their corresponding characters using **FontForge**, which generates the final font file.

### 6. Preview & Export

The generated font can be previewed in the UI, renamed, and downloaded as a **.ttf file**.

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/wbutterfliez/handwriting-font-generator.git
cd handwriting-font-generator
```

### 2️⃣ Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Install required tools

Install these system tools:

* **Potrace**
* **FontForge**

Ensure both are available in your system PATH.

---

**Turn your handwriting into a font. ✍️**
