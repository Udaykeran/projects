import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageTk  # Add this import statement
import io
from PIL import Image
import tempfile
from PIL import Image
import numpy as np
class ImageToSketchConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Sketch Converter")
        
        self.image_path = ""
        
        # Create GUI elements
        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)
        
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()
        
        self.line_thickness_scale = tk.Scale(root, label="Line Thickness", from_=1, to=10, orient="horizontal")
        self.line_thickness_scale.pack(pady=5)
        
        self.contrast_scale = tk.Scale(root, label="Contrast", from_=0.5, to=2, resolution=0.1, orient="horizontal")
        self.contrast_scale.pack(pady=5)
        
        self.brightness_scale = tk.Scale(root, label="Brightness", from_=0.5, to=2, resolution=0.1, orient="horizontal")
        self.brightness_scale.pack(pady=5)
        
        self.convert_button = tk.Button(root, text="Convert to Sketch", command=self.convert_to_sketch)
        self.convert_button.pack(pady=10)
        
        self.save_button = tk.Button(root, text="Save Sketch", command=self.save_sketch)
        self.save_button.pack(pady=10)
        
        self.preview_sketch = None
        
    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        self.show_image()
        
    def show_image(self):
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.image.thumbnail((400, 400))
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        
    def convert_to_sketch(self):
        if self.image_path:
            # Apply sketch-like filters
            grayscale_image = self.image.convert("L")
            inverted_image = ImageOps.invert(grayscale_image)
            sketch_image = ImageOps.invert(inverted_image)
            
            # Enhance contrast and brightness
            contrast_factor = self.contrast_scale.get()
            brightness_factor = self.brightness_scale.get()
            
            # Enhance contrast first, then enhance brightness
            sketch_image = ImageEnhance.Contrast(sketch_image).enhance(contrast_factor)
            sketch_image = ImageEnhance.Brightness(sketch_image).enhance(brightness_factor)
            
            # Create PhotoImage instance and store it as an attribute
            self.preview_sketch = ImageTk.PhotoImage(sketch_image)
            
            # Display the sketch on canvas
            self.canvas.create_image(0, 0, anchor="nw", image=self.preview_sketch)
        else:
            messagebox.showerror("Error", "Please upload an image first.")


    def save_sketch(self):
        if self.preview_sketch:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if save_path:
                # Convert PhotoImage to PIL Image
                pil_image = self._photo_image(self.preview_sketch)
                
                # Save the PIL Image to the specified file path
                pil_image.save(save_path)
                
                messagebox.showinfo("Success", f"Sketch saved successfully at {save_path}")
                print("Sketch saved successfully at:", save_path)  # Debugging statement
        else:
            messagebox.showerror("Error", "No sketch to save. Please convert an image first.")

    def _photo_image(self, img):
        """Convert a PhotoImage object to a PIL Image."""
        from PIL import ImageTk

        # Convert PhotoImage to PIL Image
        pil_img = ImageTk.getimage(img)

        return pil_img

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToSketchConverter(root)
    root.mainloop()
