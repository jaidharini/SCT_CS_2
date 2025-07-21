import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os
import random

def encrypt_image(input_path, key, output_name):
    output_dir = os.path.join(os.path.dirname(input_path), "output")
    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(input_path)
    data = np.array(img)

    h, w, c = data.shape
    flat_data = data.reshape(-1, c)

    random.seed(key)
    indices = list(range(len(flat_data)))
    random.shuffle(indices)

    scrambled_data = flat_data[indices]
    scrambled_data ^= key

    encrypted_data = scrambled_data.reshape(h, w, c)
    encrypted_img = Image.fromarray(encrypted_data)
    encrypted_path = os.path.join(output_dir, output_name)
    encrypted_img.save(encrypted_path)
    return encrypted_path, indices

def decrypt_image(encrypted_path, key, output_name, indices):
    output_dir = os.path.join(os.path.dirname(encrypted_path), "output")
    os.makedirs(output_dir, exist_ok=True)

    encrypted_img = Image.open(encrypted_path)
    encrypted_data = np.array(encrypted_img)

    h, w, c = encrypted_data.shape
    flat_encrypted = encrypted_data.reshape(-1, c)

    flat_encrypted ^= key

    original_data = np.zeros_like(flat_encrypted)
    for i, idx in enumerate(indices):
        original_data[idx] = flat_encrypted[i]

    decrypted_data = original_data.reshape(h, w, c)
    decrypted_img = Image.fromarray(decrypted_data)
    decrypted_path = os.path.join(output_dir, output_name)
    decrypted_img.save(decrypted_path)
    return decrypted_path

class ImageCipherApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Encrypt/Decrypt")
        self.indices = None

        tk.Label(master, text="Key:").grid(row=0, column=0)
        self.key_entry = tk.Entry(master)
        self.key_entry.grid(row=0, column=1)

        self.load_button = tk.Button(master, text="Choose Image", command=self.load_image)
        self.load_button.grid(row=1, column=0, columnspan=2)
        self.encrypt_button = tk.Button(master, text="Encrypt", command=self.encrypt)
        self.encrypt_button.grid(row=2, column=0)
        self.decrypt_button = tk.Button(master, text="Decrypt", command=self.decrypt)
        self.decrypt_button.grid(row=2, column=1)

        self.image_label = tk.Label(master)
        self.image_label.grid(row=3, column=0, columnspan=2)

        self.img_path = ""
        self.encrypted_path = ""

    def load_image(self):
        self.img_path = filedialog.askopenfilename(title="Select image", 
                                                   filetypes=(("PNG files","*.png"),("All files","*.*")))
        if self.img_path:
            img = Image.open(self.img_path)
            img.thumbnail((250, 250))
            self.tk_img = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.tk_img)
            self.image_label.image = self.tk_img

    def encrypt(self):
        if not self.img_path or not self.key_entry.get():
            messagebox.showinfo("Error", "Please select an image and enter a key.")
            return
        key = int(self.key_entry.get())
        self.encrypted_path, self.indices = encrypt_image(self.img_path, key, "encrypted.png")
        messagebox.showinfo("Success", f"Encrypted image saved to {self.encrypted_path}")

    def decrypt(self):
        if not self.encrypted_path or self.indices is None or not self.key_entry.get():
            messagebox.showinfo("Error", "No encrypted image or key found. Encrypt something first.")
            return
        key = int(self.key_entry.get())
        decrypted_path = decrypt_image(self.encrypted_path, key, "decrypted.png", self.indices)
        img = Image.open(decrypted_path)
        img.thumbnail((250, 250))
        self.tk_img = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_img)
        self.image_label.image = self.tk_img
        messagebox.showinfo("Success", f"Decrypted image saved to {decrypted_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCipherApp(root)
    root.mainloop()
