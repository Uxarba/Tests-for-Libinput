To use this script:

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
