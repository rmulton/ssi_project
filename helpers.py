'''
Helper functions for readable code.
You should only have to use :
    - increment_cfg(...) that decides how the radio config should change at every step.
    - init_radio(...) that initiate a radio program.
'''
from microbit import display
import radio

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
    if radio_mode=='ble':
        radio.ble()
    elif radio_mode=='raw':
        radio.config(raw=1)
    chan = chan_min - 1
    rate_nb = 0
    return radio, chan, rate_nb
