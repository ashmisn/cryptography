import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import hashlib

# Function to encode the message into the image
def encode_message():
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("PNG files", "*.png")])
    if not image_path:
        return

    message = message_entry.get("1.0", tk.END).strip()
    password = password_entry.get().strip()

    if not message or not password:
        messagebox.showwarning("Input Error", "Please enter both a message and a password.")
        return

    # Hash the password for verification during decryption
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    combined_message = password_hash + "::" + message

    img = Image.open(image_path)
    binary_msg = ''.join(format(ord(char), '08b') for char in combined_message) + '1111111111111110'
    pixels = list(img.getdata())

    if len(binary_msg) > len(pixels):
        messagebox.showerror("Error", "Message is too long to encode in the selected image.")
        return

    new_pixels = [((pixel[0] & ~1) | int(binary_msg[i]), *pixel[1:]) if i < len(binary_msg) else pixel
                  for i, pixel in enumerate(pixels)]

    img.putdata(new_pixels)
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        img.save(save_path)
        messagebox.showinfo("Success", f"Message successfully hidden and saved to:\n{save_path}")

# GUI setup for encryption
root = tk.Tk()
root.title("Image Steganography - Encrypt")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

header = tk.Label(root, text="🔒 Encrypt Message into Image", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white")
header.pack(fill="x", pady=10)

entry_frame = tk.Frame(root, bg="#f5f5f5")
entry_frame.pack(pady=15)

message_label = tk.Label(entry_frame, text="Enter message:", font=("Arial", 12), bg="#f5f5f5")
message_label.grid(row=0, column=0, sticky="w")
message_entry = tk.Text(entry_frame, height=4, width=50, font=("Arial", 10))
message_entry.grid(row=1, column=0, padx=10, pady=5)

password_label = tk.Label(entry_frame, text="Enter password:", font=("Arial", 12), bg="#f5f5f5")
password_label.grid(row=2, column=0, sticky="w")
password_entry = tk.Entry(entry_frame, show="*", font=("Arial", 10), width=40)
password_entry.grid(row=3, column=0, padx=10, pady=5)

encode_btn = tk.Button(root, text="🔑 Encrypt Image", command=encode_message, bg="#2196F3", fg="white", font=("Arial", 12))
encode_btn.pack(pady=10)

footer = tk.Label(root, text="Developed with ❤️ in Python", font=("Arial", 10), bg="#f5f5f5", fg="#555")
footer.pack(side="bottom", pady=10)

root.mainloop()