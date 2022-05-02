import canvas.log as log
import requests
import json

# the following code made me question my connection to reality, fuck you twitch

def auth(account, channel):
    if channel == "":
        cid = 465810007
    else:
        cid = requests.get(f"https://api.ivr.fi/twitch/resolve/{channel}").json()["id"]
    
    auth = account.split(':')
    headers = {
        "Authorization": auth[0],
        "Client-Id": auth[1],
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36" # surely they wont ban me Clueless
    }
    with open("canvas/jsons/getut.json") as f:
        body = json.loads(f.read())
        body["variables"]["channelID"] = str(cid)

    r = requests.post("https://gql.twitch.tv/gql", json=body, headers=headers).json()
    exts = r["data"]["user"]["channel"]["selfInstalledExtensions"] # gets all installed extensions in the given channel
    for ext in exts:
        if ext["installation"]["id"].split(":")[0] == "9jjigdr1wlul7fbginbq7h76jg9h3s": # finds the extension with the streamcanvas extension id
            jwt = ext["token"]["jwt"] # this gets the jwt token from gql (i have no idea what jwt means but apparently its used for authorisation with extensions?)

    with open("canvas/jsons/getet.json") as f:
        body = json.loads(f.read())
        body["variables"]["token"] = jwt
        body["variables"]["channelID"] = str(cid)

    token = requests.post("https://gql.twitch.tv/gql", json=body, headers=headers).json()["data"]["extensionLinkUser"]["token"]["jwt"] # this ACTUALLY gets the extension auth token, i have no idea why twitch requires another token just to get this but thats just twitch ig 
    log.info("Authenticated account " + account)
    return token # finally

