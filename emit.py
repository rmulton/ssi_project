from microbit import display
import radio
from helpers import init_radio, increment_cfg

# Inputs
CHAN_MIN = 38
CHAN_MAX = 47
RADIO_MODE = 'ble'
DEST_ADDR = ''
EMIT_ADDR = ''
DATARATES = [
    radio.RATE_250KBIT,
    radio.RATE_1MBIT,
    radio.RATE_2MBIT
    ]
PKT_TO_SEND = bytes([0x40, 0x42, 0xd8, 0x2a, 0x41, 0x32, 0x65,0x02, 0x01, 0x1a, 0x09, 0x09])+b'DEFCON25'

# Initiate the radio module
radio, chan, rate_nb = init_radio(RADIO_MODE, CHAN_MIN)

while True:
    cfg_str, chan, rate_nb = increment_cfg(radio, chan, rate_nb, CHAN_MIN, CHAN_MAX, DATARATES)
    radio.send(PKT_TO_SEND)
    print('{} || Packet sent {}'.format(cfg_str, PKT_TO_SEND))