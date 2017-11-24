'''
Code that displays packets regarding the inputs.
'''
from microbit import display
# Radio module modded by radiobit team
import radio

##############
### Inputs ###
##############

# Change these ones
CHAN_MIN = 0 # Min 0
CHAN_MAX = 100 # Max 100
DEST_ADDR_FILTER = '' # ex: 88:c6 or 88

# Probably not to change
DATARATES = [
    radio.RATE_250KBIT,
    radio.RATE_1MBIT,
    radio.RATE_2MBIT
    ]
RADIO_MODE = 'ble'

# Experimental
RESEND_MODE = False
DISPLAY_RAW = False
EMIT_ADDR_FILTER = '' # the addr recognized is rarely the good one
DISPLAY_SENDER = False

###############
### Helpers ###
###############

# Update radio configuration parameters
def _increment_cfg_param(chan, rate_nb, chan_min, chan_max, datarates):
    '''
    Increment radio config parameters : bluetooth channel, datarate.
    '''
    chan += 1
    if chan>chan_max:
        chan = chan_min
        rate_nb += 1
    if rate_nb>len(datarates)-1:
        rate_nb = 0
    rate = datarates[rate_nb]
    return chan, rate_nb, rate

# Update radio configuration
def increment_cfg(radio, chan, rate_nb, chan_min, chan_max, datarates):
    if chan_min!=chan_max:
        chan, rate_nb, rate = _increment_cfg_param(chan, rate_nb, chan_min, chan_max, datarates)
        radio.config(channel=chan, data_rate=rate)
    cfg_str = 'Channel : {} || Datarate : {}'.format(chan, rate_nb)
    return cfg_str, chan, rate_nb

# Initiate the radio module
def init_radio(radio_mode, chan_min):
    '''
    Display starting messages. Set radio config before the loop.
    '''
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

######################
### Packet readers ###
######################

# Different functions to parse the packets
def _packet_to_string_unknown_format(pkt):
    '''
    Get a printable string from packet for unknown packet formats.
    '''
    rest = ' '.join(['%02x '%c for c in pkt])
    return rest

def _packet_to_string_rb_format(pkt):
    '''
    Get a printable string from packet for the packet format described by the radiobit team.
    '''
    dest_addr = '%02x:%02x:%02x:%02x:%02x:%02x' % (
    pkt[13], pkt[12], pkt[11], pkt[10], pkt[9], pkt[8]
    )
    if len(pkt)>39:
        sender_addr = '%02x:%02x:%02x:%02x:%02x:%02x' % (
        pkt[34], pkt[35], pkt[36], pkt[37], pkt[38], pkt[39]
        )
    elif DISPLAY_SENDER:
        sender_addr = 'unrecognized'
    advinfo = ' '.join(['%02x '%c for c in pkt[14:]])
    rest = ' '.join(['%02x '%c for c in pkt[:8]])
    return dest_addr, sender_addr, 'Address : {} || Sender : {} || Adv_info : {}  || Rest : {}'.format(dest_addr, sender_addr, advinfo, rest)

# Main function
def read_pkt(pkt, dest_addr_filter, emit_addr_filter):
    '''
    One function to read different kinds of packet. Returns a string to be printed.
    '''
    try:
        # Packets in the format given by radiobit repo
        if len(pkt) >= 13:
            dest_filter_size = len(dest_addr_filter)
            emit_filter_size = len(emit_addr_filter)
            dest_addr, emit_addr, pkt_str = _packet_to_string_rb_format(pkt)
            # Filter packets regarding the destination address and emiter address filters
            if dest_addr[:dest_filter_size]==dest_addr_filter and emit_addr[:emit_filter_size]==emit_addr_filter:
                return pkt_str
            else:
                return None
        # Other formats
        else:
            pkt_str = _packet_to_string_unknown_format(pkt)
            return pkt_str
    # Some packets look too long to display
    except MemoryError as e:
        return 'Error : packet is too long, couldnt display'

#################
### Main code ###
#################

# Initiate
radio, chan, rate_nb = init_radio(RADIO_MODE, CHAN_MIN)

# Loop
while True:

    # Update channel and datarate
    cfg_str, chan, rate_nb = increment_cfg(radio, chan, rate_nb, CHAN_MIN, CHAN_MAX, DATARATES)

    # Receive packets
    pkt = radio.receive_bytes()

    # Display packets
    if pkt is not None:
        if RESEND_MODE:
            print('>> Resent')
            radio.send_bytes(pkt)
        pkt_str = read_pkt(pkt, DEST_ADDR_FILTER, EMIT_ADDR_FILTER)
        if pkt_str:
            try:
                if DISPLAY_RAW:
                    print('Raw :\n {} \n {} || {}'.format(pkt, cfg_str, pkt_str))
                else:
                    print('{} || {}'.format(cfg_str, pkt_str))
            except MemoryError as e:
                print('Error : packet is too long, couldnt display')
           