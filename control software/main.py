"""
    - WeeKey control main file
    - Naomi Silver September 2025
    - V1.0
"""

import yaml
import os
import keyboard
import time
import subprocess
import threading
import win32api
from win32con import VK_MEDIA_PLAY_PAUSE, VK_MEDIA_NEXT_TRACK, VK_MEDIA_PREV_TRACK, KEYEVENTF_EXTENDEDKEY, KEYEVENTF_KEYUP, VK_VOLUME_DOWN, VK_VOLUME_MUTE, VK_VOLUME_UP

SCRIPT_FILE = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_FILE, "config.yml") 

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    return config.get("keys", {})

def bind_keys(key_map):
    try:
        for key, action in key_map.items(): # for each key and action in key_map
            keyboard.add_hotkey(key, lambda a=action: handle_action(a))
    except AttributeError: # dont error if there isnt an action 
        print("keybind needs action")

def handle_action(action): # action handling
    try:

        if action.startswith("run:"): 
            cmd = action[4:].strip() # strip the command part of the config setup
            subprocess.Popen(cmd, shell=False) # run shell command to open

        elif action.startswith("type:"):
            text = action[5:].strip()
            keyboard.write(text)

        elif action.startswith("media:"):
            media = action[6:].strip()
            if media == ("play_pause"):
                win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0); win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_KEYUP, 0) # press and release using win32api
                time.sleep(0.2) # additional debounce, stops it from rapidly pausing and unpausing
            if media == ("next"):
                win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0, 0); win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_KEYUP, 0)
                time.sleep(0.2)
            if media == ("previous"):
                win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0, 0); win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0, KEYEVENTF_KEYUP, 0)
                time.sleep(0.2)
            if media == ("vol_mute"):
                win32api.keybd_event(VK_VOLUME_MUTE, 0, KEYEVENTF_EXTENDEDKEY); win32api.keybd_event(VK_VOLUME_MUTE, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP)
                time.sleep(0.2)

        elif action.startswith("shortcut:"):
            shortcut = action[9:].strip()
            keyboard.press_and_release(shortcut)
            time.sleep(0.2)

        elif action.startswith("browser:"):
            url = action[8:].strip()
            os.startfile(url)

        else:
            print("not valid macro")

    except AttributeError: # doesnt crash if the keybind doesnt have action, crashes if something else is wrong
        print("keybind needs action")

def key_updater(): # update the config and key binds to refresh every 5 seconds
    while True:
        key_map = load_config()
        bind_keys(key_map)
        time.sleep(5)
        keyboard.unhook_all_hotkeys() # remove old hotkeys
        # print("hotkeys reloaded")


def main():
    thread = threading.Thread(target=key_updater, daemon=True) # new thread 
    thread.start()

    keyboard.wait()


if __name__ == "__main__":
    main()