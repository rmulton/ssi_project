# ssi_project
This project aims to sniff and inject bluetooth low energy (BLE) using a micro:bit.
We are using radiobit's from project code. See their work here : https://github.com/virtualabs/radiobit. 

## Installation
### 1. Get a micro:bit
### 2. Clone radiobit repo
``` git clone https://github.com/virtualabs/radiobit ```
### 3. Install uflash
``` pip install uflash ```
### 4. Install a serial communication program
To be able to see what the micro:bit prints, you need to use the serial communication interface.
See here : https://www.microbit.co.uk/td/serial-library
#### MacOS and GNU/Linux
For macos and linux users, you are going to use ```screen```
1. Install screen.
2. Attach a screen to the micro:bit serial communication system.

```ls /dev/cu.usb*``` will give you the serial communication system name (not tested on GNU/Linux).

```screen /dev/cu.usb<replace with micro:bit name> 115200``` will attach a screen to the micro:bit serial communication system.

Then you should be good to go !

If there is a problem connecting to the device, you probably need to kill a current detached screen with ```pkill screen```

You can check the current living screens with ```screen -ls```
### 5. Flash the micro:bit
Now you can flash the micro:bit with our program and the radiobit firmware.

```uflash -r <replace with the path to radiobit repo>/radiobit/precompiled/radiobit.hex  <replace with the path to this repo>/ssi_project/<program_you_want_to_use>.py```

Example : ```uflash -r .\radiobit\precompiled\radiobit.hex .\ssi_project\snif.py```

### 6. Our contribution
- Sniffer for logs: ```snif_raw_version.py```
This one is used to sniff all received packets and print them in a log. The corresponding notebook for analysis is in ```./logs/Analysis.ipynb```

- Sniffer for live observation: ```snif.py```

- You can find logs in ```./logs/```
