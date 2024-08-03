import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageEnhance
import threading

class ImageUpscalerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Upscaler")
        self.root.geometry("500x600")

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select Image", command=self.select_image)
        self.select_button.pack(pady=5)

        self.scale_label = tk.Label(root, text="Upscale Factor (e.g., 2 for 2x):")
        self.scale_label.pack(pady=5)
        self.scale_entry = tk.Entry(root)
        self.scale_entry.pack(pady=5)

        self.upscale_button = tk.Button(root, text="Upscale Image", command=self.start_upscale, state=tk.DISABLED)
        self.upscale_button.pack(pady=5)

        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Upscaled Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(pady=5)

        self.original_image = None
        self.upscaled_image = None

    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_thumbnail(self.original_image)
            self.upscale_button.config(state=tk.NORMAL)

    def display_thumbnail(self, image):
        thumbnail = image.copy()
        thumbnail.thumbnail((400, 400))
        self.image_tk = ImageTk.PhotoImage(thumbnail)
        self.image_label.config(image=self.image_tk)

    def start_upscale(self):
        try:
            scale_factor = float(self.scale_entry.get())
            if scale_factor <= 0:
                raise ValueError("Scale factor must be greater than 0")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the upscale factor.")
            return

        self.progress['value'] = 0
        threading.Thread(target=self.upscale_image, args=(scale_factor,)).start()

    def upscale_image(self, scale_factor):
        width, height = self.original_image.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        # Upscale the image
        self.upscaled_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Apply sharpening filter
        enhancer = ImageEnhance.Sharpness(self.upscaled_image)
        self.upscaled_image = enhancer.enhance(2.0)

        self.progress['value'] = 100
        self.display_thumbnail(self.upscaled_image)
        self.save_button.config(state=tk.NORMAL)

    def save_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path and self.upscaled_image:
            self.upscaled_image.save(save_path)
            messagebox.showinfo("Image Saved", "Upscaled image saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageUpscalerApp(root)
    root.mainloop()
