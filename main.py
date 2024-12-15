import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import os

class ImageReductionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Reduction Tool")
        self.root.geometry("800x600")
        self.original_image = None
        self.processed_image = None
        self.create_widgets()

    def create_widgets(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        tk.Button(control_frame, text = "Select Image", command = self.load_image).pack(side = tk.LEFT, padx = 5)
        tk.Label(control_frame, text = "Reduction Method:").pack(side = tk.LEFT, padx = 5)
        self.reduction_method = tk.StringVar(value = "Lanczos")
        reduction_methods = ["Nearest", "Bilinear", "Bicubic", "Lanczos"]
        reduction_dropdown = ttk.Combobox(control_frame, textvariable = self.reduction_method, 
                                          values = reduction_methods, width = 10)
        reduction_dropdown.pack(side = tk.LEFT, padx = 5)

        tk.Label(control_frame, text = "Reduction Factor:").pack(side = tk.LEFT, padx = 5)
        self.reduction_factor = tk.Scale(control_frame, from_ = 2, to = 10, 
                                         orient = tk.HORIZONTAL, length = 100)
        self.reduction_factor.set(5)
        self.reduction_factor.pack(side = tk.LEFT, padx = 5)

        tk.Button(control_frame, text = "Reduce Image", command = self.reduce_image).pack(side = tk.LEFT, padx = 5)
        tk.Button(control_frame, text = "Save Image", command = self.save_image).pack(side = tk.LEFT, padx = 5)

        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(expand = True, fill = tk.BOTH, padx = 10, pady = 10)

        self.original_label = tk.Label(self.image_frame)
        self.original_label.pack(side = tk.LEFT, expand = True, fill = tk.BOTH, padx = 5)

        self.processed_label = tk.Label(self.image_frame)
        self.processed_label.pack(side = tk.RIGHT, expand = True, fill = tk.BOTH, padx = 5)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_image(self.original_image, self.original_label)
                self.processed_label.config(image = '')
                self.processed_image = None
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")

    def reduce_image(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please select an image first")
            return

        k = self.reduction_factor.get()
        method_map = {
            "Nearest": Image.NEAREST,
            "Bilinear": Image.BILINEAR,
            "Bicubic": Image.BICUBIC,
            "Lanczos": Image.LANCZOS
        }
        method = method_map[self.reduction_method.get()]

        width = max(1, int(self.original_image.width / k))
        height = max(1, int(self.original_image.height / k))
        self.processed_image = self.original_image.resize((width, height), method)
        
        self.display_image(self.processed_image, self.processed_label)
        messagebox.showinfo("Reduction Complete", 
            f"Original Size: {self.original_image.size}\n"
            f"Reduced Size: {self.processed_image.size}\n"
            f"Reduction Factor: {k}x\n"
            f"Method: {self.reduction_method.get()}"
        )

    def display_image(self, image, label, max_width = 400, max_height = 300):
        image.thumbnail((max_width, max_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label.config(image = photo)
        label.image = photo

    def save_image(self):
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No processed image to save")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension = ".jpg",
            filetypes = [("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")],
            title = "Save Processed Image"
        )
        if not file_path:
            return
        try:
            self.processed_image.save(file_path)
            messagebox.showinfo("Success", f"Image saved to {os.path.basename(file_path)}")
        except PermissionError:
            messagebox.showerror("Error", "Permission denied. Choose a different location.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image: {e}")

def main():
    root = tk.Tk()
    app = ImageReductionApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()