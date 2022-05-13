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
    global sio,placed
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
        global x,y
        iterations = 0
        while True:
            placed = []
            x = random.randint(0,len(img[0])-1)
            y = random.randint(0,len(img)-1)
            if iterations*settings["delay"] >= 3500:
                acctoken = account.auth(acc, settings["channel"])
                iterations = 0
            if [x, y] not in placed and place(img[x][y], [settings["start"][0] + y, settings["start"][1] + x], acctoken, sio[acc]):
                placed.append([x,y])
                time.sleep(settings["delay"])
                iterations = iterations + 1

    elif settings["mode"] == "void":
        globaly
        place_at = [0,0]
        while True:
            if iterations*settings["delay"] >= 3500:
                acctoken = account.auth(acc, settings["channel"])
                iterations = 0
            time.sleep(settings["delay"])
            while place_at in placed:
                place_at = [random.randint(settings["start"][0]-int(y),settings["start"][0]+int(y)),random.randint(settings["start"][1]-int(y),settings["start"][1]+int(y))]
                y = y + settings["void_speed"]
            place([settings["void_color"], 100], place_at, acctoken, sio[acc])
            placed.append(place_at)
            iterations = iterations + 1
    else:
        log.error("Provided invalid mode.")
