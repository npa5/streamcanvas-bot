import canvas.log as log
import canvas.account as account
import threading
import random
import time
import toml
import requests
import socketio
pi = 0
i = 0
n = 0
sio = {}
placed = []

def place(color, pixel, token, sio):
    sio.emit("p", {"t": token, "x": pixel[0], "y": pixel[1], "c": color})
    log.info(f"Placed pixel {color} at {pixel}")

def loop(acc, img, size, settings):
    global sio,i,n,pi,placed
    acctoken = account.auth(acc, settings["channel"])
    sio[acc] = socketio.Client()
    sio[acc].connect(f'https://api.streamcanvas.raven.fo/{settings["channel"]}')
    log.info(f"started thread {acctoken}")

    if settings["mode"] == "image":
        while True:
            time.sleep(settings["delay"])
            place(img[i], [settings["start"][0] + pi, settings["start"][1] + n], acctoken, sio[acc])
            if n == size[1]-1:
                log.info("Completed image, restarting.")
                n = 0
                i = 0
            if not pi == size[0]:
                i = i + 1
                pi = pi + 1
            else:
                pi = 0
                n = n + 1

    elif settings["mode"] == "void":
        place_at = [0,0]
        while True:
            time.sleep(settings["delay"])
            while place_at in placed:
                place_at = [random.randint(settings["start"][0]-int(i),settings["start"][0]+int(i)),random.randint(settings["start"][1]-int(i),settings["start"][1]+int(i))]
                i = i + settings["void_speed"]
            place(settings["void_color"], [place_at[0], place_at[1]], acctoken, sio[acc])
            placed.append(place_at)
