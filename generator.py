import customtkinter as ctk
import qrcode
from PIL import Image
from tkinter import filedialog, colorchooser, messagebox

# ---- QR Generator Function ----
def choose_color(entry):
    color = colorchooser.askcolor()[1]
    if color:
        entry.delete(0, ctk.END)
        entry.insert(0, color)

def select_logo():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if path:
        logo_path_var.set(path)

def generate_qr():
    data = data_entry.get().strip()
    if not data:
        messagebox.showwarning("Input Required", "Please enter text or URL to encode.")
        return
    
    fill_color = fill_entry.get().strip() or "black"
    back_color = back_entry.get().strip() or "white"
    logo_path = logo_path_var.get()

    # Create QR Code
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    if back_color.lower() == "transparent" or back_color == "":
        qr_img = qr.make_image(fill_color=fill_color, back_color="white").convert("RGBA")
        new_data = []
        for r, g, b, *a in qr_img.getdata():
            if r > 250 and g > 250 and b > 250:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append((r, g, b, 255))
        qr_img.putdata(new_data)
    else:
        qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

    # Add logo
    if logo_path:
        try:
            logo = Image.open(logo_path).convert("RGBA")
            w, h = qr_img.size
            size = int(w * 0.2)
            logo = logo.resize((size, size))
            pos = ((w - size) // 2, (h - size) // 2)
            qr_img.paste(logo, pos, mask=logo)
        except:
            messagebox.showerror("Error", "Could not load logo.")

    # Save QR
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
    if save_path:
        qr_img.save(save_path)
        messagebox.showinfo("Success", f"QR Code saved as {save_path}")

    # Preview
    preview = qr_img.resize((200, 200))
    ctk_img = ctk.CTkImage(light_image=preview, dark_image=preview, size=(200, 200))
    preview_label.configure(image=ctk_img)
    preview_label.image = ctk_img

# ---- UI Setup ----
ctk.set_appearance_mode("dark")   # "light" or "dark"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

root = ctk.CTk()
root.title("QR Code Generator")
root.geometry("400x550")

# Title
title = ctk.CTkLabel(root, text="✨ QR Code Generator", font=("Segoe UI", 20, "bold"))
title.pack(pady=15)

# Frame
frame = ctk.CTkFrame(root)
frame.pack(padx=10, pady=10, fill="both", expand=False)

# Entries
data_entry = ctk.CTkEntry(frame, placeholder_text="Enter Text / URL")
data_entry.pack(pady=8, padx=20, fill="x")

fill_entry = ctk.CTkEntry(frame, placeholder_text="QR Color (e.g. #000000)")
fill_entry.insert(0, "black")
fill_entry.pack(pady=5, padx=20, fill="x")

fill_btn = ctk.CTkButton(frame, text="Pick QR Color", command=lambda: choose_color(fill_entry))
fill_btn.pack(pady=2)

back_entry = ctk.CTkEntry(frame, placeholder_text="Background Color or 'transparent'")
back_entry.insert(0, "white")
back_entry.pack(pady=5, padx=20, fill="x")

back_btn = ctk.CTkButton(frame, text="Pick Background", command=lambda: choose_color(back_entry))
back_btn.pack(pady=2)

# Logo Button
logo_path_var = ctk.StringVar()
logo_btn = ctk.CTkButton(frame, text="🖼️ Select Logo", command=select_logo)
logo_btn.pack(pady=10)

# Generate Button
generate_btn = ctk.CTkButton(root, text="✨ Generate QR", command=generate_qr, fg_color="#4CC9F0", hover_color="#3A97D4", font=("Segoe UI", 14, "bold"))
generate_btn.pack(pady=15)

# Preview
preview_label = ctk.CTkLabel(root, text="")
preview_label.pack(pady=10)

root.mainloop()