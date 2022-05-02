import canvas.log as log
import canvas.account as account
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

def loop(acc, img, size, start, channel):
    global sio
    global i
    global n
    global pi
    acctoken = account.auth(acc, channel)
    conf = toml.load("config.toml")
    sio[acc] = socketio.Client()
    sio[acc].connect(f'https://api.streamcanvas.raven.fo/{conf["settings"]["channel"]}')
    log.info(f"started thread {acctoken}")

    while True:
        if img[i] != "000000":
            time.sleep(conf["settings"]["delay"])
            place(img[i], [start[0] + pi, start[1] + n], acctoken, sio[acc])

        if n == size[1]:
            exit()

        if not pi == size[0]:
            i = i + 1
            pi = pi + 1
        else:
            acctoken = account.auth(acc, channel) # this should prevent all tokens from expiring
            pi = 0
            n = n + 1

