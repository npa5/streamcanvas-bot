from canvas import log
import requests
import time

def check(channel, users):
    while True:
        r = requests.get(f'https://tmi.twitch.tv/group/user/{channel}/chatters').json()
        for group in r['chatters']:
            for user in r['chatters'][group]:
                if user in users:
                    log.info(f'User {user} found in viewerlist, shutting down bot.')
                    exit()
        if 'mods' in users:
            for mod in r['chatters']['moderators']:
                isbot = requests.get(f'https://api.ivr.fi/twitch/resolve/{mod}').json()['bot']
                if isbot == False:
                    log.info('Mod found in viewerlist, shutting down bot.')
                    exit()
        time.sleep(60)