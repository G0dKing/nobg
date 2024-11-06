import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import rembg
import io
import os
import tempfile
import shutil
from tkinterdnd2 import TkinterDnD, DND_FILES

def how_to_use():
    messagebox.showinfo("How to Use", '''Why Not Photoshop? \nBecause removing backgrounds in Photoshop is annoying af when it's a similar color to the subject.\nInstructions: \nSelect an image file, click the button.''')

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:  # Check if a file is selected
        display_image(file_path)

def on_submit():
    try:
        processed_image = remove_background(current_file_path)
        if processed_image:
            display_before_after_images(current_file_path, processed_image)
        else:
            messagebox.showinfo("Processing Error", "Image processing failed.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the image: {e}")

def remove_background(image_path):
    try:
        with open(image_path, "rb") as input_file:
            input_data = input_file.read()
        output_data = rembg.remove(input_data)
        return Image.open(io.BytesIO(output_data))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove background: {e}")
        return None

def display_image(file_path):
    global current_file_path
    current_file_path = file_path.strip('{}')
    try:
        image = Image.open(current_file_path)
        image = image.resize((500, 500), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(image)

        image_label.config(image=tk_image)
        image_label.image = tk_image

        submit_button.config(command=on_submit)
        submit_button.pack(pady=5)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open the image: {e}")

def save_temp_image(processed_image):
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, "removed_bg.png")
    processed_image.save(temp_path)
    return temp_path

def on_drop(event):
    file_path = event.data.strip('{}')  # Remove any surrounding braces
    display_image(file_path)

def display_before_after_images(original_path, processed_image):
    global temp_removed_bg_path, result_window
    result_window = tk.Toplevel(window)
    result_window.title("Before And After Images")

    try:
        # Original Image
        original_image = Image.open(original_path)
        original_image = original_image.resize((500, 500), Image.LANCZOS)
        tk_original_image = ImageTk.PhotoImage(original_image)

        # Processed Image
        processed_image = processed_image.resize((500, 500), Image.LANCZOS)
        tk_processed_image = ImageTk.PhotoImage(processed_image)

        # Before and After Label
        before_after_label = tk.Label(result_window, text="Before And After", font=("Georgia", 14))
        before_after_label.pack(pady=5)

        # Display Original Image
        original_label = tk.Label(result_window, image=tk_original_image)
        original_label.image = tk_original_image
        original_label.pack(side="left", padx=10)

        # Display Processed Image
        processed_label = tk.Label(result_window, image=tk_processed_image)
        processed_label.image = tk_processed_image
        processed_label.pack(side="left", padx=10)

        # Download Button
        download_button = tk.Button(result_window, text="Download", command=download_image)
        download_button.pack(pady=5)

        # Close Button
        close_button = tk.Button(result_window, text="Cancel", command=result_window.destroy)
        close_button.pack(pady=5)

        # Save the processed image path in temporary storage
        temp_removed_bg_path = save_temp_image(processed_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display images: {e}")

def download_image():
    global temp_removed_bg_path, result_window
    if temp_removed_bg_path:
        destination_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if destination_path:
            shutil.copy(temp_removed_bg_path, destination_path)
            messagebox.showinfo("Save Successful", f"Image saved to {destination_path}")
            result_window.destroy()  # Close the Before and After window
            window.deiconify()  # Show the main window again
        else:
            messagebox.showinfo("Save Cancelled", "Image not saved.")

# Creating Main Window with TkinterDnD
window = TkinterDnD.Tk()
window.title("Alex Pariah's Background Removal Tool")
window.minsize(width=300, height=350)

logo_image = tk.PhotoImage(file="no_bg_logo.png")
logo_image_resized = logo_image.subsample(2, 2)
logo_label = tk.Label(window, image=logo_image_resized)
logo_label.pack(pady=10)  # Add padding on the Y-axis

menu_bar = tk.Menu(window)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Home", menu=file_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=how_to_use)
menu_bar.add_cascade(label="How To Use", menu=help_menu)

more_features = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="More Features", menu=more_features)

page_title = tk.Label(window, text="Upload Your Picture Here", font=("Georgia", 18))
page_title.pack()

# Bind the drag-and-drop events
window.drop_target_register(DND_FILES)
window.dnd_bind('<<Drop>>', on_drop)

# Button to open the file dialog
browse_button = tk.Button(window, text="Browse", command=browse_file)
browse_button.pack(pady=5)

# Label to display the selected image
image_label = tk.Label(window)
image_label.pack(pady=10)

# Create "Remove Background" button outside display_image function
submit_button = tk.Button(window, text="Remove Background", command=on_submit)

window.config(menu=menu_bar)
window.mainloop()