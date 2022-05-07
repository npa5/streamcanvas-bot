import toml
import requests
import canvas.log as log

def load():
    try:
        config = toml.load("config.toml") # Attempts to load config file, creates new if not found
    except Exception: # BatChest USE "EXCEPT EXEPTION:"!!!!!
        log.warn("Config file not found/syntax error; creating new config.")
        with open("config.toml", "w") as f:
            f.write(requests.get("https://pastebin.com/raw/Zv9hryQj").text) # Gets config file from pastebin and writes it to config file
        log.info("Got default configuration and wrote it to config.toml.")
        config = toml.load("config.toml") # Loads config from current config file

    log.info("Successfully loaded config.")
    return config
