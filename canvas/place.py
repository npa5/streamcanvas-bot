import canvas.log as log
import threading
import time
import toml
import requests
import socketio
global sio
global i
global n
global pi
pi = 0
i = 0
n = 0
sio = {}

def place(color, pixel, token, sio):
    sio.emit("p", {"t": token, "x": pixel[0], "y": pixel[1], "c": color})
    log.info(f"Placed pixel {color} at {pixel}")

def loop(acc, img, size, start):
    global sio
    global i
    global n
    global pi
    conf = toml.load("config.toml")
    sio[acc] = socketio.Client() # Creates socketio client
    sio[acc].connect(f'https://api.streamcanvas.raven.fo/{conf["settings"]["channel"]}') # Connect to streamcanvas api
    log.info(f"started thread {acc}")

    while True:
        if img[i] != "000000": # skips pixel if transparent (yes i know fully black pixels get skipped too but im too lazy to change this rn)
            time.sleep(conf["settings"]["delay"])
            place(img[i], [start[0] + pi, start[1] + n], acc, sio[acc])

        if not pi == size[0]:
            i = i + 1
            pi = pi + 1
        else:
            pi = 0
            n = n + 1

