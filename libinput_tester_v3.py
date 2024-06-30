#!/usr/bin/env python3
# Key changes in this version:
# Added a new "Append Log" button next to the "Save Log" button.
# Created a new method _save_log that handles both saving and appending to the log file.
# Modified the save_log and added a new append_log method, both of which call _save_log with different modes ('w' for write, 'a' for append).
# Used filedialog.asksaveasfilename to allow the user to choose where to save the log file and what to name it.
# Added feedback messages to inform the user whether the log was saved or appended.
# Increased the initial window size to 700x400 to accommodate the new button.
# 
# To use this script:
#
# Save it as libinput_tester.py.
# Make sure you have the required libraries installed:
# Copysudo pip3 install evdev
# 
# Run the script with sudo privileges:
# Copysudo python3 libinput_tester.py
# Now, when you run the script, you'll have two options for saving the log:
# "Save Log" will create a new file or overwrite an existing file.
# Append Log" will add the new events to the end of an existing file (or create a new file if it doesn't exist).
# Both options will open a file dialog where you can choose the location and name of the log file. This provides more flexibility in managing the log files and # # # allows for accumulating data over multiple testing sessions.

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog
import evdev
import os
import threading
import time

class LibinputTester:
    def __init__(self, master):
        self.master = master
        master.title("Libinput Event Tester")

        # Configure the grid
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        # Create a frame for the text area
        text_frame = ttk.Frame(master)
        text_frame.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        # Create the text area
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD)
        self.text_area.grid(row=0, column=0, sticky="nsew")

        # Create a frame for buttons
        button_frame = ttk.Frame(master)
        button_frame.grid(row=1, column=0, columnspan=5, sticky="ew", padx=10, pady=5)
        for i in range(5):
            button_frame.columnconfigure(i, weight=1)

        # Create buttons
        self.start_button = ttk.Button(button_frame, text="Start Testing", command=self.start_testing)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop Testing", command=self.stop_testing, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_text)
        self.clear_button.grid(row=0, column=2, padx=5)

        self.save_button = ttk.Button(button_frame, text="Save Log", command=self.save_log)
        self.save_button.grid(row=0, column=3, padx=5)

        self.append_button = ttk.Button(button_frame, text="Append Log", command=self.append_log)
        self.append_button.grid(row=0, column=4, padx=5)

        self.testing = False
        self.log = []

        # Set minimum size for the window
        master.update()
        master.minsize(master.winfo_width(), master.winfo_height())

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
        self._save_log(mode='w')

    def append_log(self):
        self._save_log(mode='a')

    def _save_log(self, mode='w'):
        if not self.log:
            messagebox.showinfo("Info", "No events to save.")
            return

        home_dir = os.path.expanduser("~")
        initial_dir = os.path.join(home_dir, "libinput_events.log")
        filename = filedialog.asksaveasfilename(
            initialdir=home_dir,
            initialfile="libinput_events.log",
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, mode) as f:
                for event in self.log:
                    f.write(event + "\n")
            messagebox.showinfo("Info", f"Log {'saved to' if mode == 'w' else 'appended to'} {filename}")

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
    root.geometry("700x400")  # Set initial size
    root.mainloop()

if __name__ == "__main__":
    main()
