import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# calculate the blur score of an image
def calculate_blur_score(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var

# process images and collect blurry ones
def process_images(folder_path, blur_threshold):
    blurry_images = []
    total_images = 0

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            if image is None:
                continue

            total_images += 1
            blur_score = calculate_blur_score(image)
            if blur_score < blur_threshold:
                blurry_images.append(image_path)

    return blurry_images, total_images

# display blurry images in a slideshow with delete option
def display_blurry_images(blurry_images):
    if not blurry_images:
        messagebox.showinfo("No Blurry Images", "No blurry images found below the threshold.")
        return

    slideshow = tk.Toplevel(root)
    slideshow.title("Blurry Images Viewer")
    
    current_index = [0]  # Using a list to make it mutable

    def update_image():
        if not blurry_images:
            messagebox.showinfo("No More Images", "All blurry images have been deleted.")
            slideshow.destroy()
            return

        image_path = blurry_images[current_index[0]]
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img.thumbnail((800, 600))  # Resize for better viewing
        imgtk = ImageTk.PhotoImage(img)
        label_image.config(image=imgtk)
        label_image.image = imgtk
        label_path.config(text=os.path.basename(image_path))

    def next_image():
        if current_index[0] < len(blurry_images) - 1:
            current_index[0] += 1
            update_image()

    def prev_image():
        if current_index[0] > 0:
            current_index[0] -= 1
            update_image()

    def delete_current_image():
        if blurry_images:
            image_path = blurry_images[current_index[0]]
            os.remove(image_path)
            blurry_images.pop(current_index[0])
            if current_index[0] >= len(blurry_images):
                current_index[0] = len(blurry_images) - 1
            update_image()

    # GUI Components
    label_image = tk.Label(slideshow)
    label_image.pack(pady=10)

    label_path = tk.Label(slideshow, text="", wraplength=600)
    label_path.pack(pady=5)

    frame_controls = tk.Frame(slideshow)
    frame_controls.pack(pady=10)

    btn_prev = tk.Button(frame_controls, text="Previous", command=prev_image)
    btn_prev.grid(row=0, column=0, padx=10)

    btn_next = tk.Button(frame_controls, text="Next", command=next_image)
    btn_next.grid(row=0, column=1, padx=10)

    btn_delete = tk.Button(slideshow, text="Delete This Image", command=delete_current_image)
    btn_delete.pack(pady=10)

    update_image()

# open folder selection dialog
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        try:
            blur_threshold = float(entry_threshold.get())
            blurry_images, total_images = process_images(folder_path, blur_threshold)
            messagebox.showinfo("Processing Complete", f"Processed {total_images} images.\nFound {len(blurry_images)} blurry images.")
            if blurry_images:
                display_blurry_images(blurry_images)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the blur threshold.")

# GUI Setup
root = tk.Tk()
root.title("Blur Image Detection and Deletion")

# Blur Threshold Label and Entry
label_threshold = tk.Label(root, text="Blur Threshold (e.g., 100):")
label_threshold.pack(pady=5)
entry_threshold = tk.Entry(root)
entry_threshold.pack(pady=5)
entry_threshold.insert(0, "100")  # Default blur threshold value

# Folder Button
button_select_folder = tk.Button(root, text="Select Folder and Process", command=select_folder)
button_select_folder.pack(pady=20)

# Run the GUI
root.mainloop()