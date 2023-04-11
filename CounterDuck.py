import os
import sys
import time
import keyboard
import win32com.client
import pyautogui
import ctypes
from ctypes import wintypes
import subprocess
from pynput import keyboard
import win32com.client

# Get a handle to the console window
console_window = ctypes.windll.kernel32.GetConsoleWindow()

# Hide the console window
if console_window:
    ctypes.windll.user32.ShowWindow(console_window, 0)

def eject_device_with_serial_id(serial_id):
    # Convert the serial ID to a Unicode string
    serial_id = serial_id.encode('utf-16-le')

    # Call the Windows API function CM_Locate_DevNodeW to get a handle to the device
    devinst = ctypes.c_void_p()
    res = ctypes.windll.cfgmgr32.CM_Locate_DevNodeW(ctypes.byref(devinst), serial_id, 0)

    if res != 0:
        print(f"Failed to locate device with serial ID {serial_id}")
        return

    # Call the Windows API function CM_Request_Device_Eject to eject the device
    res = ctypes.windll.cfgmgr32.CM_Request_Device_EjectW(devinst, None, None, None, 0)

    if res != 0:
        print(f"Failed to eject device with serial ID {serial_id}")
    else:
        print(f"Device with serial ID {serial_id} ejected")

def on_start_devices():
    # initialize the list of connected device serial IDs
    serial_ids = []

    while True:
        # get the current list of connected device serial IDs
        current_ids = []
        wmi = win32com.client.GetObject("winmgmts:")
        for usb in wmi.InstancesOf("Win32_USBHub"):
            serial_id = usb.DeviceID.split("\\")[-1]
            current_ids.append(serial_id)

        # check for new devices
        for serial_id in current_ids:
            if serial_id not in serial_ids:

                eject_device_with_serial_id(serial_id)

                message_box_title = "Attention!"
                message_box_message = "New USB device detected! Device has been disconnected."
                message_box_style = ctypes.c_uint(0x00000000 | 0x00000040)  # OK button

                # Show the message box
                ctypes.windll.user32.MessageBoxW(None, message_box_message, message_box_title, message_box_style)

        # check for devices with the keyword "flip" in the serial ID
        for serial_id in current_ids:
            if "flip" in serial_id.lower():
                eject_device_with_serial_id(serial_id)

                message_box_title = "Attention!"
                message_box_message = "Flipper Zero detected. Device has been disconnected."
                message_box_style = ctypes.c_uint(0x00000000 | 0x00000040)  # OK button

                # Show the message box
                ctypes.windll.user32.MessageBoxW(None, message_box_message, message_box_title, message_box_style)

        # update the list of connected device serial IDs
        serial_ids = current_ids
        print(serial_ids)

        # wait for a short delay before checking again
        time.sleep(1)


def on_key_press(key):
    global key_count, last_key_press_time, input_allowed

    # Increment the key count and get the current time
    key_count += 1
    current_time = time.time()

    # Calculate the time difference since the last key press
    time_diff = current_time - last_key_press_time

    if time_diff > 0.04: # 0.04 equals 1/25, so 25 keys per second, change it if you want
        
        key_presses_per_sec = key_count / time_diff

        # If there are more than 25 key presses per second
        if key_presses_per_sec > 25:

            # Define message box parameters
            message_box_title = "Attention!"
            message_box_message = "Potential Badusb attack detected, input will be disturbed for 15 seconds!"
            message_box_style = ctypes.c_uint(0x00000000 | 0x00000040 | 0x00001000)  # OK button and topmost window

            # Show the message box
            ctypes.windll.user32.MessageBoxW(None, message_box_message, message_box_title, message_box_style)

            # Simulate pressing the Windows key to block all input
            pyautogui.press('win')

            # Wait for 15 seconds
            time.sleep(15)

            # Simulate pressing the Windows key again to unblock input
            pyautogui.press('win')
            
        # Reset the key count and last key press time
        key_count = 0
        last_key_press_time = current_time

# Create a keyboard listener
listener = keyboard.Listener(on_press=on_key_press)

# Start the listener
listener.start()
key_count = 0
last_key_press_time = time.time()

# Keep the script running to allow the listener to capture key presses
while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        # Stop the listener if Ctrl-C is pressed
        listener.stop()
        break
