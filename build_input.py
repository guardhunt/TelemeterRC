import evdev

def build_device():
    """
        check all input devices currently connected
        select X-Box controller if found
        return evdev device
    """

    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        if device.name == "Microsoft X-Box pad":
            device = evdev.InputDevice(device.fn)

        try:
            device
        except NameError:
            print("No X-Box controller found")
            pass
        else:
            print(str(device.name + " found"))
            return device

def build_config(device):
    """
        build and return configuration dictionary for device
    """
    capabilities = device.capabilities(verbose=True)
    config = {}

    for key, value in capabilities.items():
        for element in value:
            if type(element[0]) is tuple:
                config[element[0][1]] = element[0][0]
            elif type(element[0]) is list:
                config[element[1]] = element[0][0]
            elif ("SYN" in str(element[0])) or ("FF" in str(element[0])):
                pass
            else:
                config[element[1]] = element[0]

    print("Config Dict: " + str(config) + "\n")
    return config

def build_state(device, config):
    """
        build and return state dictionary for device
        initialize all keys to capability name of device
        initialize all values to zero
    """
    capaRAW = device.capabilities(absinfo=False)
    state = {}

    for code in capaRAW[1]:
        state[config[code]] = 0

    for code in capaRAW[3]:
        state[config[code]] = 0

    print("State Dict: " + str(state))
    return state
