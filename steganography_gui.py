import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# Encode the message into the image
def encode_message():
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("PNG files", "*.png")])
    if not image_path:
        return

    message = text_entry.get("1.0", tk.END).strip()
    if not message:
        messagebox.showwarning("Input Error", "Please enter a message to hide.")
        return

    img = Image.open(image_path)
    binary_msg = ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'
    pixels = list(img.getdata())

    new_pixels = []
    msg_index = 0
    for pixel in pixels:
        if msg_index < len(binary_msg):
            new_pixel = (pixel[0] & ~1 | int(binary_msg[msg_index]), *pixel[1:])
            new_pixels.append(new_pixel)
            msg_index += 1
        else:
            new_pixels.append(pixel)

    img.putdata(new_pixels)
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        img.save(save_path)
        messagebox.showinfo("Success", f"Message successfully hidden and saved to:\n{save_path}")

# Decode the message from the image
def decode_message():
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("PNG files", "*.png")])
    if not image_path:
        return

    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_msg = ''.join(str(pixel[0] & 1) for pixel in pixels)
    message = ""

    for i in range(0, len(binary_msg), 8):
        byte = binary_msg[i:i+8]
        if byte == '11111110':
            break
        message += chr(int(byte, 2))

    messagebox.showinfo("Hidden Message", f"Extracted Message:\n{message}")

# GUI setup
root = tk.Tk()
root.title("Image Steganography")
root.geometry("400x300")
root.resizable(False, False)

# Widgets
label = tk.Label(root, text="Enter message to hide:")
label.pack(pady=10)

text_entry = tk.Text(root, height=5, width=40)
text_entry.pack(pady=5)

encode_btn = tk.Button(root, text="Encode Message", command=encode_message, width=20)
encode_btn.pack(pady=10)

decode_btn = tk.Button(root, text="Decode Message", command=decode_message, width=20)
decode_btn.pack(pady=5)

root.mainloop()
