from microbit import display, running_time
import radio

### Inputs ###
CHAN_MIN = 37 # Min 0
CHAN_MAX = 50 # Max 100
DATARATES = [
    radio.RATE_250KBIT,
    radio.RATE_1MBIT,
    radio.RATE_2MBIT
    ]
RADIO_MODE = 'ble'
### Helpers ###
def read_pkt_mem_err(pkt, chan, rate_nb):
    print(running_time())
    print(chan)
    print(rate_nb%3)
    print('.')
    for el in pkt:
        print(hex(el))
    print('\n')
    return

# Initiate the radio module
def init_radio(radio_mode, chan_min):
    # Display starting messages
    display.scroll('>>')
    print('\n >> Starting ... \n')
    # Start and configure the radio
    radio.on()
    radio.config(channel=chan_min)
    if radio_mode=='ble':
        radio.ble()
    elif radio_mode=='raw':
        radio.config(raw=1)
    chan = chan_min - 1
    rate_nb = 0
    return radio, chan, rate_nb

### Main code ###

# Initiate
radio, chan, rate_nb = init_radio(RADIO_MODE, CHAN_MIN)
rate = DATARATES[0]
start = running_time()
# Loop
while True:
    # Increment
    chan += 1
    if chan>CHAN_MAX:
        chan = CHAN_MIN
        rate_nb += 1
        rate = DATARATES[rate_nb%3]
    radio.config(channel=chan, data_rate=rate)
    # Receive packets
    pkt = radio.receive_bytes()
    # Display packets
    if pkt is not None:
        read_pkt_mem_err(pkt, chan, rate_nb)
 