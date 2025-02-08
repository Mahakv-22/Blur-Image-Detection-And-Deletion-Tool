import os
import cv2
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askdirectory

def is_image_blurry(image_path, threshold=100):
    """
    Check if the image is blurry using the Laplacian variance method.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return False  # Skip if the image cannot be read

    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
    return laplacian_var < threshold

def detect_blurry_images(folder_path, threshold=100):
    """
    Detect blurry images in a given folder and suggest deletion.
    """
    blurry_images = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                if is_image_blurry(file_path, threshold):
                    blurry_images.append(file_path)

    return blurry_images

def main():
    print("Select your mobile gallery folder.")
    Tk().withdraw()  # Hide the root Tkinter window
    folder_path = askdirectory(title="Select Gallery Folder")
    
    if not folder_path:
        print("No folder selected. Exiting.")
        return

    threshold = 100  # Adjust the threshold for your requirements
    print("Detecting blurry images...")
    blurry_images = detect_blurry_images(folder_path, threshold)

    if blurry_images:
        print("\nThe following images are detected as blurry:")
        for img_path in blurry_images:
            print(img_path)

        print("\nConsider deleting the blurry images to save space.")
    else:
        print("\nNo blurry images detected.")

if __name__ == "__main__":
    main()


# from flask import Flask, render_template, request
# import os
# import cv2
# from werkzeug.utils import secure_filename

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# def is_image_blurry(image_path, threshold=100):
#     """
#     Check if the image is blurry using the Laplacian variance method.
#     """
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if image is None:
#         return False  # Skip if the image cannot be read
#     laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
#     return laplacian_var < threshold

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     blurry_images = []
#     files = request.files.getlist('images')

#     for file in files:
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)

#         if is_image_blurry(filepath):
#             blurry_images.append(filename)

#     return render_template('result.html', blurry_images=blurry_images)

# if __name__ == '__main__':
#     app.run(debug=True)
