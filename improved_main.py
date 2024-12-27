import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import os

class ImageReductionApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Image Reduction Tool")
        self.root.geometry("800x600")
        self.original_image = None
        self.processed_image = None
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.create_widgets()

    def create_widgets(self):
        control_frame = ctk.CTkFrame(self.root)
        control_frame.pack(side="top", fill="x", padx=10, pady=10)

        ctk.CTkButton(control_frame, text="Select Image", command=self.load_image).pack(side="left", padx=5)
        
        ctk.CTkLabel(control_frame, text="Reduction Method:").pack(side="left", padx=5)
        self.reduction_method = ctk.StringVar(value="Lanczos")
        reduction_methods = ["Nearest", "Bilinear", "Bicubic", "Lanczos"]
        reduction_dropdown = ctk.CTkOptionMenu(control_frame, variable=self.reduction_method, 
                                             values=reduction_methods, width=120)
        reduction_dropdown.pack(side="left", padx=5)

        ctk.CTkLabel(control_frame, text="Reduction Factor:").pack(side="left", padx=5)
        self.reduction_factor = ctk.CTkSlider(control_frame, from_=2, to=10, 
                                            number_of_steps=8, width=120)
        self.reduction_factor.set(5)
        self.reduction_factor.pack(side="left", padx=5)

        ctk.CTkButton(control_frame, text="Reduce Image", command=self.reduce_image).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="Save Image", command=self.save_image).pack(side="left", padx=5)

        self.image_frame = ctk.CTkFrame(self.root)
        self.image_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.original_label = ctk.CTkLabel(self.image_frame, text="")
        self.original_label.pack(side="left", expand=True, fill="both", padx=5)

        self.processed_label = ctk.CTkLabel(self.image_frame, text="")
        self.processed_label.pack(side="right", expand=True, fill="both", padx=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_image(self.original_image, self.original_label)
                self.processed_label.configure(image=None)
                self.processed_image = None
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")

    def reduce_image(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please select an image first")
            return

        k = int(self.reduction_factor.get())
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

    def display_image(self, image, label, max_width=400, max_height=300):
        display_copy = image.copy()
        display_copy.thumbnail((max_width, max_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(display_copy)
        label.configure(image=photo)
        label.image = photo

    def save_image(self):
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No processed image to save")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")],
            title="Save Processed Image"
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

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageReductionApp()
    app.run()