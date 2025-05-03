import cv2
import pytesseract
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pywhatkit
import threading
from datetime import datetime
import time

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global variables
stop_sending = False
phone_numbers = []

# OCR number extraction
def extract_numbers_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []

    frame_count = 0
    numbers_found = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 10 != 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        raw_numbers = re.findall(r'(\+91[\s\-]?\d{5}[\s\-]?\d{5})', text)

        for num in raw_numbers:
            clean = re.sub(r'[^\d+]', '', num)
            if re.fullmatch(r'\+91\d{10}', clean):
                numbers_found.add(clean)

    cap.release()
    return sorted(numbers_found)

# Message sending logic
def send_messages():
    global stop_sending
    if not phone_numbers:
        messagebox.showerror("No Numbers", "No phone numbers extracted.")
        return

    msg = message_entry.get("1.0", tk.END).strip()
    media_path = media_var.get()

    if not msg and not media_path:
        messagebox.showerror("Empty Fields", "Enter a message or choose a media file.")
        return

    status_text.insert(tk.END, "📤 Sending messages...\n")
    status_text.see(tk.END)
    status_text.update()

    def send_all():
        global stop_sending
        success_count = 0
        fail_count = 0
        is_image = media_path.lower().endswith(('.png', '.jpg', '.jpeg'))

        for number in phone_numbers:
            if stop_sending:
                status_text.insert(tk.END, "\n🛑 Sending stopped by user.\n")
                status_text.see(tk.END)
                status_text.update()
                return

            try:
                if media_path and is_image:
                    pywhatkit.sendwhats_image(number, media_path, msg or " ", wait_time=10, tab_close=True)
                elif media_path and not is_image:
                    status_text.insert(tk.END, f"⚠️ Unsupported media for {number}: Only images allowed. Skipping.\n")
                    pywhatkit.sendwhatmsg_instantly(number, msg or " ", wait_time=10, tab_close=True)
                else:
                    pywhatkit.sendwhatmsg_instantly(number, msg or " ", wait_time=10, tab_close=True)

                status_text.insert(tk.END, f"✅ Sent to {number}\n")
                success_count += 1
            except Exception as e:
                status_text.insert(tk.END, f"❌ Failed for {number}: {str(e)}\n")
                fail_count += 1

            status_text.see(tk.END)
            status_text.update()
            time.sleep(10)

        status_text.insert(tk.END, f"\n🎉 Sent: {success_count}, Failed: {fail_count}\n")
        status_text.see(tk.END)
        status_text.update()
        messagebox.showinfo("Done", f"✅ Sent: {success_count}\n❌ Failed: {fail_count}")

    threading.Thread(target=send_all).start()

def stop_sending_messages():
    global stop_sending
    stop_sending = True

def browse_video():
    path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    if path:
        video_var.set(path)
        status_text.insert(tk.END, "🔍 Extracting numbers...\n")
        status_text.see(tk.END)
        status_text.update()
        global phone_numbers
        phone_numbers = extract_numbers_from_video(path)
        phone_list.delete(0, tk.END)
        if phone_numbers:
            for num in phone_numbers:
                phone_list.insert(tk.END, num)
            status_text.insert(tk.END, f"✅ Found {len(phone_numbers)} valid numbers.\n")
        else:
            status_text.insert(tk.END, "❌ No valid numbers found.\n")
        status_text.see(tk.END)
        status_text.update()

def browse_media():
    path = filedialog.askopenfilename(filetypes=[("Media files", "*.jpg *.png *.mp4 *.pdf *.docx")])
    if path:
        media_var.set(path)

def add_number():
    num = add_number_entry.get().strip()
    if num:
        if num.startswith("+91"):
            num = "+91" + num[3:]
        elif num.startswith("91") and len(num) == 12:
            num = "+" + num
        elif len(num) == 10:
            num = "+91" + num
        elif not num.startswith("+91"):
            num = "+91" + num

        if re.fullmatch(r'\+91\d{10}', num):
            if num not in phone_numbers:
                phone_numbers.append(num)
                phone_list.insert(tk.END, num)
                status_text.insert(tk.END, f"✅ Added {num}\n")
            else:
                status_text.insert(tk.END, f"⚠️ {num} already exists.\n")
        else:
            status_text.insert(tk.END, "❌ Invalid number format.\n")
    status_text.see(tk.END)
    status_text.update()

def remove_number():
    selected = phone_list.curselection()
    if selected:
        index = selected[0]
        num = phone_list.get(index)
        phone_list.delete(index)
        phone_numbers.remove(num)
        status_text.insert(tk.END, f"🗑️ Removed {num}\n")
        status_text.see(tk.END)
        status_text.update()

def find_number():
    num = find_number_entry.get().strip()
    if num.startswith("+91") and len(num) == 13:
        pass
    elif len(num) == 10:
        num = "+91" + num

    if num in phone_numbers:
        index = phone_numbers.index(num)
        phone_list.selection_clear(0, tk.END)
        phone_list.selection_set(index)
        phone_list.see(index)
        status_text.insert(tk.END, f"🔍 Found {num}\n")
    else:
        status_text.insert(tk.END, f"❌ {num} not found\n")
    status_text.see(tk.END)
    status_text.update()

def toggle_entry(which):
    if which == "add":
        find_number_entry.grid_remove()
        add_number_entry.delete(0, tk.END)
        add_number_entry.grid()
        add_number_entry.focus_set()
    elif which == "search":
        add_number_entry.grid_remove()
        find_number_entry.delete(0, tk.END)
        find_number_entry.grid()
        find_number_entry.focus_set()

def add_number_event(event):
    add_number()
    add_number_entry.delete(0, tk.END)
    add_number_entry.grid_remove()

def find_number_event(event):
    find_number()
    find_number_entry.delete(0, tk.END)
    find_number_entry.grid_remove()

# GUI Setup
root = tk.Tk()
root.title("📞 Ravi Sir Promotion GUI")
root.geometry("720x700")
root.configure(bg="#f4f4f4")

video_var = tk.StringVar()
media_var = tk.StringVar()

# File and message input
tk.Label(root, text="🎥 Video File:", bg="#f4f4f4").pack(anchor='w', padx=10, pady=(10, 0))
tk.Entry(root, textvariable=video_var, width=60).pack(padx=10)
tk.Button(root, text="Browse Video", command=browse_video).pack(pady=5)

tk.Label(root, text="📝 Message:", bg="#f4f4f4").pack(anchor='w', padx=10)
message_entry = tk.Text(root, height=5, width=60)
message_entry.pack(padx=10)

tk.Label(root, text="📎 Optional Media File:", bg="#f4f4f4").pack(anchor='w', padx=10)
tk.Entry(root, textvariable=media_var, width=60).pack(padx=10)
tk.Button(root, text="Browse Media", command=browse_media).pack(pady=5)

# Phone list
tk.Label(root, text="📋 Extracted Numbers:", bg="#f4f4f4").pack(anchor='w', padx=10)
phone_list = tk.Listbox(root, height=6, width=60)
phone_list.pack(padx=10, pady=(0, 5))

# Buttons and inputs
button_frame = tk.Frame(root, bg="#f4f4f4")
button_frame.pack(pady=5)

add_button = tk.Button(button_frame, text="➕", command=lambda: toggle_entry("add"))
remove_button = tk.Button(button_frame, text="➖", command=remove_number)
search_button = tk.Button(button_frame, text="🔍", command=lambda: toggle_entry("search"))

add_button.grid(row=0, column=0, padx=5)
remove_button.grid(row=0, column=1, padx=5)
search_button.grid(row=0, column=2, padx=5)

add_number_entry = tk.Entry(button_frame, width=20)
find_number_entry = tk.Entry(button_frame, width=20)

add_number_entry.grid(row=0, column=3, padx=5)
find_number_entry.grid(row=0, column=4, padx=5)

add_number_entry.grid_remove()
find_number_entry.grid_remove()

add_number_entry.bind("<Return>", add_number_event)
find_number_entry.bind("<Return>", find_number_event)

# Send & Stop
tk.Button(root, text="🚀 Send Message", command=send_messages, bg="green", fg="white").pack(pady=10)
tk.Button(root, text="🛑 Stop Sending", command=stop_sending_messages, bg="red", fg="white").pack(pady=5)

# Status box
status_text = scrolledtext.ScrolledText(root, height=10, width=85)
status_text.pack(padx=10, pady=5)
status_text.insert(tk.END, "✅ Ready\n")

root.mainloop()
