#!/usr/bin/env python3

import tkinter as tk
from tkinter import scrolledtext, messagebox
import evdev
import os
import threading
import time

class LibinputTester:
    def __init__(self, master):
        self.master = master
        master.title("Libinput Event Tester")

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack(padx=10, pady=10)

        self.start_button = tk.Button(master, text="Start Testing", command=self.start_testing)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Stop Testing", command=self.stop_testing, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.clear_button = tk.Button(master, text="Clear", command=self.clear_text)
        self.clear_button.pack(pady=5)

        self.save_button = tk.Button(master, text="Save Log", command=self.save_log)
        self.save_button.pack(pady=5)

        self.testing = False
        self.log = []

    def start_testing(self):
        self.testing = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.test_events, daemon=True).start()

    def stop_testing(self):
        self.testing = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def clear_text(self):
        self.text_area.delete(1.0, tk.END)
        self.log = []

    def save_log(self):
        if not self.log:
            messagebox.showinfo("Info", "No events to save.")
            return

        home_dir = os.path.expanduser("~")
        filename = os.path.join(home_dir, "libinput_events.log")
        with open(filename, "w") as f:
            for event in self.log:
                f.write(event + "\n")
        messagebox.showinfo("Info", f"Log saved to {filename}")

    def test_events(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            self.log_event(f"Device: {device.name}, Path: {device.path}")

        while self.testing:
            for device in devices:
                try:
                    for event in device.read():
                        if event.type != evdev.ecodes.EV_SYN:
                            event_str = f"Device: {device.name}, Event: {evdev.categorize(event)}, Time: {event.timestamp()}"
                            self.log_event(event_str)
                except BlockingIOError:
                    pass
                except Exception as e:
                    self.log_event(f"Error: {str(e)}")
            time.sleep(0.01)

    def log_event(self, event_str):
        self.log.append(event_str)
        self.text_area.insert(tk.END, event_str + "\n")
        self.text_area.see(tk.END)

def main():
    root = tk.Tk()
    app = LibinputTester(root)
    root.mainloop()

if __name__ == "__main__":
    main()
