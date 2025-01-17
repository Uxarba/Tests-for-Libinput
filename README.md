To use this script:
.v3
Key changes in this version: Added a new "Append Log" button next to the "Save Log" button.
Created a new method _save_log that handles both saving and appending to the log file.
Modified the save_log and added a new append_log method, both of which call _save_log with different modes ('w' for write, 'a' for append).
Used filedialog.asksaveasfilename to allow the user to choose where to save the log file and what to name it.
Added feedback messages to inform the user whether the log was saved or appended.
Increased the initial window size to 700x400 to accommodate the new button.

To use this script:

Save it as libinput_tester.py.
Make sure you have the required libraries installed:
sudo pip3 install evdev

Run the script with sudo privileges:
sudo python3 libinput_tester.py


Now, when you run the script, you'll have two options for saving the log:

"Save Log" will create a new file or overwrite an existing file.
"Append Log" will add the new events to the end of an existing file (or create a new file if it doesn't exist).

Both options will open a file dialog where you can choose the location and name of the log file. This provides more flexibility in managing the log files and allows for accumulating data over multiple testing sessions.

.v2
Key changes in this version:

We've switched to using grid layout manager instead of pack. This allows for more flexible resizing.
The main window and the text frame are now configured to expand both horizontally and vertically when the window is resized.
We've added columnconfigure and rowconfigure to make sure that the text area expands to fill available space.
The buttons are now placed in a separate frame at the bottom of the window, which will maintain its size while the text area expands.
We've set a minimum size for the window to prevent it from being resized too small.
We've set an initial size for the window (600x400 pixels), but you can adjust this as needed.
We've used ttk widgets for a more modern look that matches the system theme.

To use this script:

Save it as libinput_tester.py.
Make sure you have the required libraries installed:
sudo pip3 install evdev

Run the script with sudo privileges:
sudo python3 libinput_tester.py


Now, when you run the script, you'll be able to resize the window, and the text area will expand or shrink accordingly. The buttons will remain at the bottom of the window. This should provide a more flexible and user-friendly interface for testing libinput events.
Save it as libinput_tester.py.
Make sure you have the required libraries installed. You can install them using pip:
Copysudo pip3 install evdev

Run the script with sudo privileges (needed to access input devices):
Copysudo python3 libinput_tester.py


This script does the following:

Creates a GUI window with a text area to display events, and buttons to start/stop testing, clear the log, and save the log.
When you click "Start Testing", it begins capturing events from all input devices recognized by libinput.
It displays the events in real-time in the text area, including the device name, event details, and timestamp.
You can stop the testing at any time by clicking "Stop Testing".
The "Clear" button clears the text area and the internal log.
The "Save Log" button saves all captured events to a file named libinput_events.log in your home directory.

Please note:

This script needs to be run with sudo privileges to access input devices.
It captures events from all input devices, which might include keyboards, mice, touchpads, etc.
The script uses threading to keep the GUI responsive while capturing events.
The log file is saved in the user's home directory, even when run with sudo.

This script should work on Debian or GNOME systems, providing a GUI interface to test and record libinput events.




