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

# Set path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global variable to control the sending process
stop_sending = False

# Extract valid +91 phone numbers from video using OCR
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

# Send WhatsApp messages to all numbers
def send_messages():
    global stop_sending
    if not phone_numbers:
        messagebox.showerror("No Numbers", "No phone numbers extracted.")
        return

    msg = message_entry.get("1.0", tk.END).strip()
    if not msg:
        messagebox.showerror("Empty Message", "Please enter a message.")
        return

    media_path = media_var.get()
    status_text.insert(tk.END, "📤 Sending messages...\n")
    status_text.update()

    def send_all():
        global stop_sending
        success_count = 0
        fail_count = 0

        for number in phone_numbers:
            if stop_sending:
                status_text.insert(tk.END, "\n🛑 Sending stopped by user.\n")
                status_text.update()
                return

            try:
                if media_path:
                    pywhatkit.sendwhats_image(number, media_path, msg, wait_time=10, tab_close=True)
                else:
                    pywhatkit.sendwhatmsg_instantly(number, msg, wait_time=10, tab_close=True)
                status_text.insert(tk.END, f"✅ Sent to {number}\n")
                success_count += 1
            except Exception as e:
                status_text.insert(tk.END, f"❌ Failed for {number}: {str(e)}\n")
                fail_count += 1

            status_text.update()
            time.sleep(10)  # Prevent overlap and WhatsApp ban risk

        status_text.insert(tk.END, f"\n🎉 Successfully sent {success_count} messages.")
        if fail_count:
            status_text.insert(tk.END, f" ❌ Failed: {fail_count}\n")
        else:
            status_text.insert(tk.END, "\n✅ All messages sent successfully.\n")
        status_text.update()

        messagebox.showinfo("Completed", f"✅ Sent: {success_count}\n❌ Failed: {fail_count}")

    threading.Thread(target=send_all).start()

# Stop sending messages
def stop_sending_messages():
    global stop_sending
    stop_sending = True

# Browse video file
def browse_video():
    path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    if path:
        video_var.set(path)
        status_text.insert(tk.END, "🔍 Extracting numbers...\n")
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
        status_text.update()

# Browse media file
def browse_media():
    path = filedialog.askopenfilename(filetypes=[("Media files", "*.jpg *.png *.mp4 *.pdf *.docx")])
    if path:
        media_var.set(path)

# GUI Setup
root = tk.Tk()
root.title("📞 WhatsApp Sender from Video OCR")
root.geometry("700x600")

video_var = tk.StringVar()
media_var = tk.StringVar()
phone_numbers = []

tk.Label(root, text="🎥 Video File:").pack(anchor='w', padx=10)
tk.Entry(root, textvariable=video_var, width=60).pack(padx=10)
tk.Button(root, text="Browse Video", command=browse_video).pack(pady=5)

tk.Label(root, text="📝 Message:").pack(anchor='w', padx=10)
message_entry = tk.Text(root, height=5, width=60)
message_entry.pack(padx=10)

tk.Label(root, text="📎 Optional Media File:").pack(anchor='w', padx=10)
tk.Entry(root, textvariable=media_var, width=60).pack(padx=10)
tk.Button(root, text="Browse Media", command=browse_media).pack(pady=5)

tk.Label(root, text="📋 Extracted Numbers:").pack(anchor='w', padx=10)
phone_list = tk.Listbox(root, height=6, width=60)
phone_list.pack(padx=10, pady=5)

tk.Button(root, text="🚀 Send Message", command=send_messages, bg="green", fg="white").pack(pady=10)
tk.Button(root, text="🛑 Stop Sending", command=stop_sending_messages, bg="red", fg="white").pack(pady=5)

status_text = scrolledtext.ScrolledText(root, height=10, width=80)
status_text.pack(padx=10, pady=5)
status_text.insert(tk.END, "✅ Ready\n")

root.mainloop()
