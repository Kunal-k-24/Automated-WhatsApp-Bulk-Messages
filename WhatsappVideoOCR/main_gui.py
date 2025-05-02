import cv2
import pytesseract
import re
import os

# Set path to Tesseract if not already in system PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Ask for video file path
video_path = input("Enter full path of the screen recording video file: ")

# Check if the file path exists
if not os.path.exists(video_path):
    print("❌ File does not exist. Please check the path.")
    exit()

# Open the video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("❌ Could not open video.")
    exit()

print("🔍 Extracting frames and reading numbers...")

extracted_numbers = set()
frame_count = 0

# Process frames from the video
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 10 != 0:
        continue  # Skip frames to speed up processing

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # OCR text extraction from the frame
    text = pytesseract.image_to_string(gray)
    print(f"\n🖼️ Frame {frame_count} OCR Text:\n{text.strip()}")

    # Improved regex for flexible number patterns
    raw_numbers = re.findall(r'(\+?\d[\d\s\-\(\)]{9,})', text)

    # Clean and normalize numbers
    for num in raw_numbers:
        clean = re.sub(r'[\s\-\(\)]', '', num)  # Remove spaces, dashes, parentheses
        if len(clean) >= 10:  # Accept only valid-length numbers
            extracted_numbers.add(clean)

cap.release()

# Final output
print("\n📋 All unique phone numbers found:")
if extracted_numbers:
    for num in sorted(extracted_numbers):
        print("✅", num)
else:
    print("❌ No valid phone numbers were found.")
