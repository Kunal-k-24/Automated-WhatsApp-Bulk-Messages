import pywhatkit
import time

def send_message_to_numbers(numbers, message="Hello from Python!", media_path=None):
    for number in numbers:
        full_number = "+91" + number  # Change to your country code
        print(f"Sending to {full_number}...")
        try:
            if media_path:
                pywhatkit.sendwhats_image(full_number, media_path, caption=message, wait_time=15)
            else:
                pywhatkit.sendwhatmsg_instantly(full_number, message, wait_time=15, tab_close=True)
            time.sleep(20)  # Give buffer between messages
        except Exception as e:
            print(f"Failed to send to {full_number}: {e}")
