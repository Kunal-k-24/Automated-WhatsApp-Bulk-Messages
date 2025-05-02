import pytesseract
import re
from PIL import Image
import cv2
import os

# Set Tesseract path here
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_phone_numbers(frames):
    all_numbers = set()
    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pil_image = Image.fromarray(gray)
        text = pytesseract.image_to_string(pil_image)
        numbers = re.findall(r'\b\d{10}\b', text)
        all_numbers.update(numbers)
    return list(all_numbers)
