import cv2
import pytesseract
import re
import os

# Set the Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Ask for video file path
video_path = input("Enter full path of the screen recording video file: ")

if not os.path.exists(video_path):
    print("❌ File does not exist. Please check the path.")
    exit()

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("❌ Could not open video.")
    exit()

print("🔍 Extracting frames and reading numbers...")

extracted_numbers = set()
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 10 != 0:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # OCR
    text = pytesseract.image_to_string(gray)
    print(f"\n🖼️ Frame {frame_count} OCR Text:\n{text.strip()}")

    # Extract numbers and log them
    numbers = re.findall(r'\b\d{10}\b', text)
    if numbers:
        print("📞 Numbers found in this frame:", numbers)
        extracted_numbers.update(numbers)
    else:
        print("🚫 No valid numbers found in this frame.")

cap.release()

# Final output
print("\n📋 All unique phone numbers found:")
if extracted_numbers:
    for num in sorted(extracted_numbers):
        print("✅", num)
else:
    print("❌ No valid phone numbers were found.")
