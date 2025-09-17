# WeeKey

---

<p align="center">
  <img src="https://i.imgur.com/DbgnDYs.jpeg" alt="Fully assembled WeeKey 9K" width="600" />
</p>

---

**WeeKey** is a macro pad with both onboard memory capabilities and fully featured control software. It uses hand soldered, regular keyboard switches and a Raspberry Pi Pico (or similar MCU) as the controller. It relies on the F13-F21 keys for input as they're unassigned in most modern software and free for the taking.

> while I have version controlled STLs hosted here, I would prefer you download them [printables.com](https://www.printables.com/model/1415910-weekey-9k) so I can get my reward points :P

---

## Features
- Fully custom 3D printed enclosure
- USB HID input handling via a Raspberry Pi Pico (or similar) with the `usb_hid` adafruit library
- Either onboard action assignment on the MCU **or** using WeeKey Control
- Hotswap angled spacer design allowing for fine tuning to the user's liking

---

## Repo structure

```text
📁 stl/                     # STL files for 3D printing
📁 control software/        # Control software source code 
📁 pico/                    # firmware used on the MCU
📄 LICENSE                  # License for software and hardware
📄 README.md                # This file
```

## Build guide and documentation

A full build guide, including wiring, assembly, dependencies, and usage instructions are available within the [GitHub Wiki](https://github.com/naomisilver/weekey/wiki). <br>
This includes:
- Bill of materials
- Assembly and soldering
- Software and firmware installation
- Configuration file management and presets

---

## Licensing

This project uses dual licensing with [MIT licensing](./LICENSE) on all code and the hardware designs are licensed under the [CC-BY-SA 4.0 License](./stl/LICENSE). Meaning you're free to use, modify and redistribute with attribution for code and licensing deritiatives of hardware designs under the same `CC-BY-SA 4.0 License`

---

## Future

While I made this project because I didn't want to buy a stream deck and is where *I* want this. I won't entirely be shelving this project. Some potential future plans consist of:
- Creating a 12K version using a key matrix as apposed to direct wire as used on the 9K version
- Updating the firmware and control software to use a custom HID report descriptor to be able to send more than the existing 12 F keys. (this isn't off the table, I made a custom HID descriptor for my previous project, [The Novostok](https://github.com/naomisilver/novostok))
- Making magnetically attaching 'addons' that could add displays, midi controls, rotary dials etc...
- Making the existing control software platform agnostic, the firmware is by default but I rely on windows specific media controls for example. Without a Mac device this may prove difficult.


