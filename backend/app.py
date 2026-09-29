from flask import Flask, request, jsonify, send_from_directory
import os

from processor import process_image


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "backend", "uploads")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "backend", "processed")


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/upload.html")
def upload_page():
    return send_from_directory(BASE_DIR, "upload.html")


@app.route("/results.html")
def results_page():
    return send_from_directory(BASE_DIR, "results.html")


@app.route("/css/<path:filename>")
def css_files(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, "css"),
        filename
    )


@app.route("/js/<path:filename>")
def js_files(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, "js"),
        filename
    )


@app.route("/images/<path:filename>")
def image_files(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, "images"),
        filename
    )


@app.route("/processed/<path:filename>")
def processed_files(filename):
    return send_from_directory(
        PROCESSED_FOLDER,
        filename
    )


@app.route("/process", methods=["POST"])
def process():

    if "image" not in request.files:
        return jsonify({
            "error": "No image was uploaded."
        }), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected."
        }), 400

    filename = file.filename

    input_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(input_path)

    try:
        process_image(
            input_path,
            PROCESSED_FOLDER
        )

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

    return jsonify({
        "success": True,
        "redirect": "/results.html"
    })


if __name__ == "__main__":
    app.run(debug=True)