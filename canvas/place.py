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
    iterations = 0
    acctoken = account.auth(acc, settings["channel"])
    sio[acc] = socketio.Client()
    sio[acc].connect(f'https://api.streamcanvas.raven.fo/{settings["channel"]}')
    log.info(f"started thread {acctoken}")

    if settings["mode"] == "print":
        iterations = 0
        while True:
            placed = []
            for i in range(len(img)):
                for n in range(len(img[i])):
                    if iterations*settings["delay"] >= 3500:
                        acctoken = account.auth(acc, settings["channel"])
                        iterations = 0
                    if [i, n] not in placed and place(img[i][n], [settings["start"][0] + n, settings["start"][1] + i], acctoken, sio[acc]):
                        placed.append([i,n])
                        time.sleep(settings["delay"])
                        iterations = iterations + 1

    elif settings["mode"] == "realistic":
        iterations = 0
        while True:
            placed = []
            n = random.randint(0,len(img[0])-1)
            i = random.randint(0,len(img)-1)
            if iterations*settings["delay"] >= 3500:
                acctoken = account.auth(acc, settings["channel"])
                iterations = 0
            if [n, i] not in placed and place(img[n][i], [settings["start"][0] + i, settings["start"][1] + n], acctoken, sio[acc]):
                placed.append([n,i])
                time.sleep(settings["delay"])
                iterations = iterations + 1

    elif settings["mode"] == "void":
        place_at = [0,0]
        while True:
            if iterations*settings["delay"] >= 3500:
                acctoken = account.auth(acc, settings["channel"])
                iterations = 0
            time.sleep(settings["delay"])
            while place_at in placed:
                place_at = [random.randint(settings["start"][0]-int(i),settings["start"][0]+int(i)),random.randint(settings["start"][1]-int(i),settings["start"][1]+int(i))]
                i = i + settings["void_speed"]
            place([settings["void_color"], 100], place_at, acctoken, sio[acc])
            placed.append(place_at)
            iterations = iterations + 1
    else:
        log.error("Provided invalid mode.")
