"""
    - WeeKey control main file
    - Naomi Silver September 2025
    - V1.3.2 - added sequenced actions, mouse actions, configurable delays on actions and repeating sequences
"""

"""
    TODO: ADD PROFILES?
    1. have multiple sets of profiles in the config file listed: profile_1...
    2. based on some input switch between profiles?
        - this could be based on an open application? watchdog for cs2.exe sort of thing
    3. 

    NOTE: config might starting getting unwieldly if I continue to add more modifiers maybe move towards how yml is actually meant to be used though will need 
          better instructions for novice users

    NOTE: the way it is set up means I have a GUI to edit the yml file to make a bit easier to setup more complicated sequences but for now that is out of scope

    BUG: I will need to refactor handle_action and add a new run_action function to allow for the repeating modifier to respect the delays within a sequence. Currently works
         fine for auto clickers and single repeating actions but misbehaves when it comes to sequences.
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
import mouse
from PIL import Image

notifs_show = False # gives the user the option to turn notifs on/off
icon = None # used for notifications
OS = sys.platform # to be used in the future when *maybe* working on cross-platform support
delay = 0.2 # this is the default, any calling in function of handle_action can then define it's own delay for repeating and sequenced actions
key_state = {}

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
            if key not in key_state:
                key_state[key] = False
            keyboard.add_hotkey(key, lambda a=action, k=key: handle_action(a, delay, key))
    except AttributeError as e: # dont error if there isnt an action 
        notify(f"Error key'{key} not assigned': {e}", icon)

def handle_action(action, delay, key): # action handling 

    print(action)
    print(key)

    try:
        if action.startswith("delay;"):
            stripped_action = action[6:].strip() # strip macro from the string
            split_action = stripped_action.split(";", 1) # split action by the first instace of a semi colon
            delay = float(split_action[0]) # convert first list item to float and update delay (if one isn't assigned, default 0.2 will be used)
            action = split_action[1] # the action following the delay item is the action to be run

        if action.startswith("run;"): 
            cmd = action[4:].strip() # strip the command part of the config setup
            time.sleep(delay)
            subprocess.Popen(cmd, shell=False) # run shell command to open
            notify(f"running command: {cmd}", icon)

        elif action.startswith("type;"):
            text = action[5:].strip()
            time.sleep(delay)
            keyboard.write(text)
            notify(f"writing text: {text}", icon)

        elif action.startswith("media;"):
            media = action[6:].strip()
            if media == ("play_pause"): 
                time.sleep(delay) # additional debounce, stops it from rapidly pausing and unpausing
                win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0); win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_KEYUP, 0) # press and release using win32api
                notify(f"running: {media}", icon)
            if media == ("next"):
                time.sleep(delay)
                win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0, 0); win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_KEYUP, 0)
                notify(f"running: {media}", icon)
            if media == ("previous"):
                time.sleep(delay)
                win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0, 0); win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0, KEYEVENTF_KEYUP, 0)
                notify(f"running: {media}", icon)
            if media == ("vol_mute"):
                time.sleep(delay)
                win32api.keybd_event(VK_VOLUME_MUTE, 0, KEYEVENTF_EXTENDEDKEY); win32api.keybd_event(VK_VOLUME_MUTE, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP)
                notify(f"running: {media}", icon)

        elif action.startswith("shortcut;"):
            shortcut = action[9:].strip()
            time.sleep(delay)
            keyboard.press_and_release(shortcut)
            notify(f"running: {shortcut}", icon)

        elif action.startswith("browser;"):
            url = action[8:].strip()
            time.sleep(delay)
            os.startfile(url)
            notify(f"opening: {url}", icon)

        elif action.startswith("mouse;"):
            mou = action[6:].strip()
            if mou.startswith("move;"):
                mou = mou[5:].strip()
                mou_list = mou.split("|") # split x and y using the delimiter |
                time.sleep(delay)
                mouse.move(mou_list[0], mou_list[1], absolute=True, duration=0) # mou_list[0]: x mou_list[1]: y 
                notify(f"moving mouse to: {mou_list}", icon)
            elif mou.startswith("click;"):
                mou = mou[6:].strip()
                time.sleep(delay)
                mouse.click(button=mou)
                mouse.release(button=mou)
                notify(f"opening: {mou}", icon)
            elif mou.startswith("double_click;"):
                mou = mou[13:].strip()
                time.sleep(delay)
                mouse.double_click(button=mou)
                notify(f"opening: {mou}", icon)

        elif action.startswith("sequence;"):
            seq = action[9:].strip()
            action_list = seq.split(",,,") # split the remaining string up using ,,, as the delimiter

            def run_sequence(actions, delay): # https://chatgpt.com/share/68d13759-c330-8013-9fa5-e8446bd90471
                for act in actions:
                    handle_action(act, delay, key) # my own implementation wouldn't run sequentially and would finish other threads before the intended one would run, didn't even think of this

            thread = threading.Thread(target=run_sequence, args=(action_list, delay), daemon=True)
            thread.start()

            #for i in range(len(action_list)):
            #    thread = threading.Thread(target=handle_action, args=(action_list[i], delay), daemon=True) 
            #    thread.start()
            #    time.sleep(delay)
            #    notify(f"starting thread for: {action_list[i]}")

        elif action.startswith("repeating;"):
            a_action = action[10:].strip()

            if key_state.get(key, False):
                key_state[key] = False
                notify(f"stopped repeating for {key}", icon)
            else:
                key_state[key] = True
                notify(f"started repeating for {key}", icon)

                def repeat_loop():
                    while key_state[key]:
                        handle_action(a_action, delay, key)
                        time.sleep(delay)
                
                thread = threading.Thread(target=repeat_loop, daemon=True).start()

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

def toggle_notifs(icon, item):
    global notifs_show
    notifs_show = not notifs_show

def notify(msg, icon=None):

    print(msg)

    if icon and notifs_show:
        try:
            icon.notify(msg)
        except Exception as e:
            print(f"Notification failed: {e}") # if the notification warning you of an error, errors at least print it :D

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