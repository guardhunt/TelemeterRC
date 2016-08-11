import struct

def encode_state(state):
    buttons1_state = 0
    buttons1_state = buttons1_state | state["BTN_A"]
    buttons1_state = buttons1_state | state["BTN_B"] << 1
    buttons1_state = buttons1_state | state["BTN_NORTH"] << 2
    buttons1_state = buttons1_state | state["BTN_WEST"] << 3
    buttons1_state = buttons1_state | state["BTN_THUMBL"] << 4
    buttons1_state = buttons1_state | state["BTN_THUMBR"] << 5

    buttons2_state = 0
    buttons2_state = buttons2_state | state["BTN_START"]
    buttons2_state = buttons2_state | state["BTN_MODE"] << 1
    buttons2_state = buttons2_state | state["BTN_SELECT"] << 2
    buttons2_state = buttons2_state | state["BTN_TR"] << 3
    buttons2_state = buttons2_state | state["BTN_TL"] << 4

    payload = struct.pack('6h2B2c', state["ABS_X"], state["ABS_Y"], state["ABS_RX"], state["ABS_RY"], state["ABS_HAT0X"], state["ABS_HAT0Y"], state["ABS_Z"], state["ABS_RZ"], buttons1_state.to_bytes(1, byteorder="big"), buttons2_state.to_bytes(1, byteorder="big"))

    return payload

def decode_packet(packet):
    buttons = []
    state = packet[14:30]
    state = struct.unpack('6h2B2c', state)

    holder1 = '{0:06b}'.format(int.from_bytes(state[8], byteorder="big"))
    holder2 = '{0:05b}'.format(int.from_bytes(state[9], byteorder="big"))

    for i in holder1:
        buttons.append(int(i))

    for  i in holder2:
        buttons.append(int(i))

    state = list(state[:7]) + buttons

    return state
