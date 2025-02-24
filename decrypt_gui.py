import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import hashlib

# Function to decode the message from the image
def decode_message():
    image_path = filedialog.askopenfilename(title="Select Encoded Image", filetypes=[("PNG files", "*.png")])
    if not image_path:
        return

    password = password_entry.get().strip()
    if not password:
        messagebox.showwarning("Input Error", "Please enter the password used during encryption.")
        return

    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_msg = ''.join(str(pixel[0] & 1) for pixel in pixels)
    extracted = ""

    for i in range(0, len(binary_msg), 8):
        byte = binary_msg[i:i+8]
        if byte == '11111110':
            break
        extracted += chr(int(byte, 2))

    try:
        stored_hash, hidden_message = extracted.split("::", 1)
    except ValueError:
        messagebox.showerror("Error", "Failed to extract message. The image may not contain a valid encoded message.")
        return

    entered_hash = hashlib.sha256(password.encode()).hexdigest()

    if stored_hash == entered_hash:
        messagebox.showinfo("Decrypted Message", f"Hidden Message:\n{hidden_message}")
    else:
        messagebox.showerror("Incorrect Password", "The password you entered is incorrect.")

# GUI setup for decryption
root = tk.Tk()
root.title("Image Steganography - Decrypt")
root.geometry("500x300")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

header = tk.Label(root, text="🔓 Decrypt Message from Image", font=("Arial", 16, "bold"), bg="#FF5722", fg="white")
header.pack(fill="x", pady=10)

entry_frame = tk.Frame(root, bg="#f5f5f5")
entry_frame.pack(pady=20)

password_label = tk.Label(entry_frame, text="Enter password:", font=("Arial", 12), bg="#f5f5f5")
password_label.pack(anchor="w")
password_entry = tk.Entry(entry_frame, show="*", font=("Arial", 10), width=40)
password_entry.pack(padx=10, pady=5)

decode_btn = tk.Button(root, text="🔍 Decrypt Image", command=decode_message, bg="#4CAF50", fg="white", font=("Arial", 12))
decode_btn.pack(pady=15)

footer = tk.Label(root, text="Developed with ❤️ in Python", font=("Arial", 10), bg="#f5f5f5", fg="#555")
footer.pack(side="bottom", pady=10)

root.mainloop()