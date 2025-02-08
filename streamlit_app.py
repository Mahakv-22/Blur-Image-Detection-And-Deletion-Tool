# # Save this as streamlit_app.py
# import streamlit as st
# import os

# st.title("Blur Image Detection App")

# folder = st.text_input("Enter the folder path:")
# threshold = st.number_input("Enter the blur threshold:", value=100)

# if st.button("Process Images"):
#     if folder and os.path.exists(folder):
#         st.write(f"Processing images in folder: {folder} with threshold {threshold}")
#         # Add your image processing logic here
#     else:
#         st.error("Invalid folder path!")

import streamlit as st
import tkinter as tk
from tkinter import filedialog
import os

# Function to open a folder selection dialog
def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    folder_path = filedialog.askdirectory()  # Open the folder selection dialog
    root.destroy()  # Close the Tkinter window
    return folder_path

# Streamlit UI
st.title("Blur Image Detection App")

# Button to trigger folder selection
if st.button("Select Folder"):
    selected_folder = select_folder()
    if selected_folder:
        st.session_state.folder = selected_folder  # Store the folder in session state
    else:
        st.warning("No folder selected!")

# Display selected folder (if any)
if "folder" in st.session_state:
    st.success(f"Selected folder: {st.session_state.folder}")
else:
    st.info("No folder selected yet.")

# Blur threshold input
threshold = st.number_input("Enter the blur threshold:", value=100)

# Process images button
if st.button("Process Images"):
    if "folder" in st.session_state and os.path.exists(st.session_state.folder):
        st.write(f"Processing images in folder: {st.session_state.folder} with threshold {threshold}")
        # Add your image processing logic here
    else:
        st.error("Please select a valid folder before processing!")
