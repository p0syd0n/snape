# snape
client to Dumbledoor remote access trojan


Uses socketio library to connect to Dumbledoor server, then periodically checks in with it. Can execute arbitrary shellcode, as well as 'curses': 

- custom tkinter messagebox

- screenshot

- play a sound(mp3 file) from the server

- do a tkinter dialog

- write text from the keyboard

- send keyboad shortcuts from the keyboard

- write messages on the keyboard: open notepad, write message, (optional): save file

- change cwd to temp

- open urls

- stream the client screen to the server, able to view stream through a link

- hydra troll

- kill tasks

## on the check-in concept
The client emits data every 2 seconds, as a way of telling the server "hey! im still here!".

The data sent by the client is a dictionary of the client id (eg: '1;2;3;4;5;6;7;8;9;0;') followed by info about the itself such as ip adress, timezone, latitude, longitude, region, city, country, current time. The format is like this:

`{
  '1;2;34;4;5;6;7;8;9;0;': 
    {
      'info': 'info',
      'more-info': 'more-info'
     }
 }`
 
Every time the server recieves a check-in, it will add the client to a dictionary of conneced clients, and then clear all duplicate keys in the dictionary.

To prevent confusion, one may force-clean the online dict by the `clear_cache` command.


More features to be added soon. 

This project was made as a newer, better version of the Dobby RAT.

