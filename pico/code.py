import board, time, digitalio, usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

button_pins = {
    "btn_1": board.GP4,
    "btn_2": board.GP3,
    "btn_3": board.GP2,
    "btn_4": board.GP7,
    "btn_5": board.GP6, # i'd intended for this to be sequential but i did each row backwards, oops. its properly defined in buttons_actions though
    "btn_6": board.GP5,
    "btn_7": board.GP10,
    "btn_8": board.GP9,
    "btn_9": board.GP8,
}

# - Within the dictionary below, you define what each button will do from top left to top right going down the keypad. Documentation on the different possibilities can be found here: https://docs.circuitpython.org/projects/hid/en/latest/api.html
# - Current it is setup to only parse some of the unused function keys in Windows, this should also mean it's platform agnostic and can be used on any machine. for more platform specific keys like command, check the documentation for what
#   keycode to use
# - This firmware is setup to be compatiable with a control software on Windows that I will get to when I can, currently I personally don't have scope to support Mac or Linux at this time.

button_actions = { # multiple actions can be assigned to one action just structure as: "[Keycode.CONTROL, Keycode.A]," up to 6 different actions will work at a time
    "btn_1": [Keycode.F13],
    "btn_2": [Keycode.F14],
    "btn_3": [Keycode.F15],
    "btn_4": [Keycode.F16],
    "btn_5": [Keycode.F17],
    "btn_6": [Keycode.F18],
    "btn_7": [Keycode.F19],
    "btn_8": [Keycode.F20], 
    "btn_9": [Keycode.F21],
}
 
buttons = {}
for name, pin in button_pins.items():
    btn = digitalio.DigitalInOut(pin)
    btn.switch_to_input(pull=digitalio.Pull.UP)
    buttons[name] = btn
   
while True:
    for name, btn in buttons.items():
        
        if not btn.value: # button pressed
            keys = button_actions[name]
            
            if isinstance(keys, (list, tuple)): # checks what type of data  is stored in keys, whether its a list or tuple (either is fine)
                kbd.press(*keys) # unpacks the list of keys from a single object from the dictionary to singular items that press() expects
            else:
                kbd.press(keys) # if it aint a list or tuple, send it all at once
                
            time.sleep(0.2) # debounce
            
            if isinstance(keys, (list, tuple)): # same again but for the release of the keys
                kbd.release(*keys)
            else:
                kbd.release(keys)
                
                
                
    
