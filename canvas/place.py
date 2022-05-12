from canvas import account,log
import threading
import random
import time
import toml
import requests
import socketio
sio = {}
i = 0

def place(color, pixel, token, sio):
    if color[1] != 0:
        sio.emit("p", {"t": token, "x": pixel[0], "y": pixel[1], "c": color[0]})
        log.info(f"Placed pixel {color} at {pixel}")
        return True
    else:
        return False

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
                    if [i, n] not in placed and place(img[i][n], [settings["start"][0] + n, settings["start"][1] + i], acctoken, sio[acc]):
                        placed.append([i,n])
                        time.sleep(settings["delay"])

    elif settings["mode"] == "realistic":
        while True:
            placed = []
            n = random.randint(0,len(img[0])-1)
            i = random.randint(0,len(img)-1)
            if [n, i] not in placed and place(img[n][i], [settings["start"][0] + i, settings["start"][1] + n], acctoken, sio[acc]):
                placed.append([n,i])
                time.sleep(settings["delay"])

    elif settings["mode"] == "void":
        place_at = [0,0]
        while True:
            time.sleep(settings["delay"])
            while place_at in placed:
                place_at = [random.randint(settings["start"][0]-int(i),settings["start"][0]+int(i)),random.randint(settings["start"][1]-int(i),settings["start"][1]+int(i))]
                i = i + settings["void_speed"]
            place([settings["void_color"], 100], place_at, acctoken, sio[acc])
            placed.append(place_at)
    else:
        log.error("Provided invalid mode.")
