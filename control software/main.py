"""
    - WeeKey control main file
    - Naomi Silver September 2025
    - V1.2.2 - fixed a bug with a crash loop when waking PC from sleep
"""

"""
    TODO:
"""

from win32con import VK_MEDIA_PLAY_PAUSE, VK_MEDIA_NEXT_TRACK, VK_MEDIA_PREV_TRACK, KEYEVENTF_EXTENDEDKEY, KEYEVENTF_KEYUP, VK_VOLUME_DOWN, VK_VOLUME_MUTE, VK_VOLUME_UP
import yaml
import os
import sys
import keyboard
import time
import subprocess
import threading
import win32api
import pystray
from PIL import Image

notifs_show = False # gives the user the option to turn notifs on/off
icon = None # used for notifications
OS = sys.platform # to be used in the future when *maybe* working on cross-platform support

def resource_path(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

def load_config():
    config_path = resource_path("config.yml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config.get("keys", {})

def bind_keys(key_map):
    try:
        for key, action in key_map.items(): # for each key and action in key_map
            keyboard.add_hotkey(key, lambda a=action: handle_action(a))
    except AttributeError as e: # dont error if there isnt an action 
        notify(f"Error key'{key} not assigned': {e}", icon)

def handle_action(action): # action handling

    try:

        if action.startswith("run:"): 
            cmd = action[4:].strip() # strip the command part of the config setup
            subprocess.Popen(cmd, shell=False) # run shell command to open
            time.sleep(0.1)
            notify(f"running command: {cmd}", icon)

        elif action.startswith("type:"):
            text = action[5:].strip()
            keyboard.write(text)
            time.sleep(0.1)
            notify(f"writing text: {text}", icon)

        elif action.startswith("media:"):
            media = action[6:].strip()
            if media == ("play_pause"): 
                win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0); win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_KEYUP, 0) # press and release using win32api
                time.sleep(0.3) # additional debounce, stops it from rapidly pausing and unpausing
                notify(f"running: {media}", icon)
            if media == ("next"):
                win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0, 0); win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_KEYUP, 0)
                time.sleep(0.3)
                notify(f"running: {media}", icon)
            if media == ("previous"):
                win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0, 0); win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0, KEYEVENTF_KEYUP, 0)
                time.sleep(0.3)
                notify(f"running: {media}", icon)
            if media == ("vol_mute"):
                win32api.keybd_event(VK_VOLUME_MUTE, 0, KEYEVENTF_EXTENDEDKEY); win32api.keybd_event(VK_VOLUME_MUTE, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP)
                time.sleep(0.3)
                notify(f"running: {media}", icon)

        elif action.startswith("shortcut:"):
            shortcut = action[9:].strip()
            keyboard.press_and_release(shortcut)
            time.sleep(0.2)
            notify(f"running: {shortcut}", icon)

        elif action.startswith("browser:"):
            url = action[8:].strip()
            os.startfile(url)
            time.sleep(0.2)
            notify(f"opening: {url}", icon)

        else:
            print("not valid macro")

    except AttributeError as e: # doesnt crash if the keybind doesnt have action, crashes if something else is wrong
        notify(f"Keybind needs action | Error: {e}", icon)
    
    except Exception as e:
        notify(f"Unexpected error: {e}", icon) 

def key_updater(): # update the config and key binds to refresh every 5 seconds
    while True:
        keyboard.add_hotkey('ctrl+shift+alt+win+tab+q', print, "dummy") # dummy hotkey to prevent crash loop one PC sleep
        keyboard.unhook_all_hotkeys() # remove old hotkeys
        key_map = load_config()
        bind_keys(key_map)
        time.sleep(5)

def on_quit(icon, item):
    icon.stop() # replaces keyboard.wait()

def open_config(icon, item):
    config_path = resource_path("config.yml") 
    if OS == "win32": # maybe working on multi-platform support?
        os.startfile(config_path)
    else:
        print("multiple OS' not working yet :D") 

def notify(msg, icon=None):

    print(msg)

    if icon and notifs_show:
        try:
            icon.notify(msg)
        except Exception as e:
            print(f"Notification failed: {e}") # if the notification warning you of an error, errors at least print it :D


def toggle_notifs(icon, item):
    global notifs_show
    notifs_show = not notifs_show

def main():
    global icon

    thread = threading.Thread(target=key_updater, daemon=True) # new thread 
    thread.start()

    icon_path = resource_path("icon.png") # crudely drawn icon :D
    icon_image = Image.open(icon_path)

    icon = pystray.Icon(
        "WeeKey",
        icon = icon_image,
        title = "WeeKey Control",
        menu = pystray.Menu(
            pystray.MenuItem("Show Notifications", toggle_notifs, checked=lambda item: notifs_show),
            pystray.MenuItem("Open Config", open_config), # on right click show "open config" option, allows for quickly editing the config
            pystray.MenuItem("Quit", on_quit), # same thing but closes the program by stopping the icon and quiting the program
        )
    )

    icon.run()

if __name__ == "__main__":
    main()