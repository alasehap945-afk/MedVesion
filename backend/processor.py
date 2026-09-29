import cv2
import os


def process_image(input_path, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    image = cv2.imread(input_path)

    if image is None:
        raise ValueError("Could not read the uploaded image.")

    # Original
    cv2.imwrite(
        os.path.join(output_folder, "original.png"),
        image
    )

    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(
        os.path.join(output_folder, "grayscale.png"),
        gray
    )

    # Contrast Enhancement
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    contrast = clahe.apply(gray)

    cv2.imwrite(
        os.path.join(output_folder, "contrast.png"),
        contrast
    )

    # Gaussian Blur
    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    cv2.imwrite(
        os.path.join(output_folder, "blur.png"),
        blur
    )

    # Edge Detection
    edges = cv2.Canny(
        blur,
        50,
        150
    )

    cv2.imwrite(
        os.path.join(output_folder, "edges.png"),
        edges
    )

    # Segmentation
    _, segmentation = cv2.threshold(
        gray,
        120,
        255,
        cv2.THRESH_BINARY
    )

    cv2.imwrite(
        os.path.join(output_folder, "segmentation.png"),
        segmentation
    )