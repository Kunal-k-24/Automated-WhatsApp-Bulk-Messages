
# Automated WhatsApp Bulk Messages

This Python application allows users to extract phone numbers from videos using Optical Character Recognition (OCR) and send bulk messages (with or without media) via WhatsApp. The app utilizes `pywhatkit` for WhatsApp automation and `pytesseract` for text extraction from video frames.

## Features:
- **Extract Phone Numbers from Video**: Extracts valid phone numbers (starting with +91) from videos using OCR.
- **Send Messages to Multiple Numbers**: Send text messages (with or without media) to the extracted phone numbers via WhatsApp.
- **Stop Sending**: Provides an option to stop the message-sending process at any time.
- **Media Support**: Attach images, videos, or documents to the message.
- **GUI Interface**: User-friendly interface built using Tkinter for easy interaction.

## Requirements:
- Python 3.x
- **Libraries**:
  - `opencv-python` (cv2)
  - `pytesseract`
  - `pywhatkit`
  - `tkinter`
  - `threading`
  - `re`

- **Tesseract OCR** installed on your system:
  - [Download Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and set the path in the script.

## Installation:

### Step 2: Install required dependencies
Run the following command to install all the necessary dependencies:
```bash
pip install opencv-python pytesseract pywhatkit
```

### Step 3: Install Tesseract OCR
1. Download and install **Tesseract OCR** from [this link](https://github.com/tesseract-ocr/tesseract).
2. After installation, make sure to set the path to Tesseract in your script:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR	esseract.exe'  # Update this path if needed
```

### Step 4: Run the app
After installing the necessary dependencies and setting up Tesseract, run the app with the following command:
```bash
python app.py
```

### Step 5: Open the application
This will open the GUI of the application where you can:
1. Browse and select a video to extract phone numbers.
2. Enter a message to send to the extracted numbers.
3. Optionally attach media files (images, videos, or documents).
4. Start sending messages to all extracted numbers with the **Send Message** button.
5. Stop the sending process at any time using the **Stop Sending** button.

## Usage:
1. **Upload a video file**: Use the "Browse Video" button to select a video file from which phone numbers need to be extracted. The app will scan the video and extract valid phone numbers starting with +91.
   
2. **Enter a message**: In the message box, enter the message you want to send to the extracted phone numbers.

3. **Optionally, attach a media file**: You can select an image, video, or document to send as an attachment by clicking on the "Browse Media" button.

4. **Send messages**: After entering the message and selecting the media (if needed), click on the **Send Message** button to start sending WhatsApp messages to all the phone numbers.

5. **Stop sending**: If you want to stop the sending process, click on the **Stop Sending** button. This will immediately stop sending any further messages.

## License:
This project is licensed under the MIT License 
