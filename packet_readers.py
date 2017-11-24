'''
Contains every functions used to parse packets.
You should only have to use read_pkt(...) function that is the interface to many packet reader functions
'''

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
    if len(pkt)>38:
        sender_addr = '%02x:%02x:%02x:%02x:%02x:%02x' % (
        pkt[34], pkt[35], pkt[36], pkt[37], pkt[38], pkt[39]
        )
    else:
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
        if len(pkt) > 13:
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
