import os
import uuid
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from preprocess import crop_grid_and_clean
from vectorize import batch_vectorize
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = "storage/uploads"
PROCESSED_DIR = "storage/processed_letters"
SVG_DIR = "storage/svg_letters"
FONTS_DIR = "storage/fonts"

for d in [UPLOAD_DIR, PROCESSED_DIR, SVG_DIR, FONTS_DIR]:
    os.makedirs(d, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB limit

FF_BIN = "fontforge"
subprocess.check_call([FF_BIN, "-script", ff_script, svg_out, out_ttf, font_name],
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)


@app.route("/upload", methods=["POST"])
def upload():
    if 'sheet' not in request.files:
        return jsonify({"error": "No file part 'sheet'"}), 400
    f = request.files['sheet']
    if f.filename == '':
        return jsonify({"error": "No selected file"}), 400

    uid = uuid.uuid4().hex[:8]
    base = os.path.join("storage", uid)
    os.makedirs(base, exist_ok=True)

    upload_path = os.path.join(base, secure_filename(f.filename))
    f.save(upload_path)

    processed_out = os.path.join(base, "processed_letters")
    svg_out = os.path.join(base, "svg_letters")
    fonts_out = os.path.join(base, "fonts")
    for d in [processed_out, svg_out, fonts_out]:
        os.makedirs(d, exist_ok=True)

    #Preprocess
    try:
        crop_grid_and_clean(upload_path, processed_out)
    except Exception as e:
        return jsonify({"step": "Preprocess", "error": str(e)}), 500

    #Vectorize
    try:
        batch_vectorize(processed_out, svg_out)
    except subprocess.CalledProcessError as e:
        return jsonify({"step": "Vectorization", "error": "Potrace failed", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"step": "Vectorization", "error": str(e)}), 500

    #FontForge font file generation
    font_name = request.form.get("font_name", "MyHandwritingFont")
    out_ttf = os.path.join(fonts_out, f"{secure_filename(font_name)}.ttf")
    try:
        ff_script = os.path.join(os.path.dirname(__file__), "generate_font_ff.py")
        subprocess.check_call([FF_BIN, "-script", ff_script, svg_out, out_ttf, font_name],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return jsonify({
            "step": "Font generation",
            "error": "FontForge failed",
            "details": str(e),
        }), 500
    except Exception as e:
        return jsonify({"step": "Font generation", "error": str(e)}), 500
    
    if not os.path.exists(out_ttf):
        return jsonify({"step": "Font generation", "error": "TTF not created"}), 500

    # Font file download
    return send_file(out_ttf, as_attachment=True, download_name=os.path.basename(out_ttf))

@app.route("/health")
def health():
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)