import canvas.log as log
import canvas.account as account
import threading
import random
import time
import toml
import requests
import socketio
sio = {}
i = 0

def place(color, pixel, token, sio):
    sio.emit("p", {"t": token, "x": pixel[0], "y": pixel[1], "c": color})
    log.info(f"Placed pixel {color} at {pixel}")

def loop(acc, img, settings):
    global sio,i,n,placed
    acctoken = account.auth(acc, settings["channel"])
    sio[acc] = socketio.Client()
    sio[acc].connect(f'https://api.streamcanvas.raven.fo/{settings["channel"]}')
    log.info(f"started thread {acctoken}")

    if settings["mode"] == "print":
        while True:
            placed = []
            for i in range(len(img)):
                for n in range(len(img[i])):
                    if img[n][i] != '000000':
                        if [n, i] not in placed:
                            placed.append([n,i])
                            place(img[n][i], [settings["start"][0] + i, settings["start"][1] + n], acctoken, sio[acc])
                            time.sleep(settings["delay"])

    elif settings["mode"] == "realistic":
        while True:
            placed = []
            print(len(img[0]))
            print(len(img))
            n = random.randint(0,len(img[0])-1)
            i = random.randint(0,len(img)-1)
            if img[n][i] != '000000':
                if [n, i] not in placed:
                    placed.append([n,i])
                    place(img[n][i], [settings["start"][0] + i, settings["start"][1] + n], acctoken, sio[acc])
                    time.sleep(settings["delay"])

    elif settings["mode"] == "void":
        place_at = [0,0]
        while True:
            time.sleep(settings["delay"])
            while place_at in placed:
                place_at = [random.randint(settings["start"][0]-int(i),settings["start"][0]+int(i)),random.randint(settings["start"][1]-int(i),settings["start"][1]+int(i))]
                i = i + settings["void_speed"]
            place(settings["void_color"], place_at, acctoken, sio[acc])
            placed.append(place_at)
    else:
        log.error("Provided invalid mode.")
