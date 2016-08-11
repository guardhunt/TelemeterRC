import socket, evdev, os.path, asyncio
from build_input import *
from appcodec import *

class RCapp():
    def __init__(self, src, dst):
        self.src = bytes(bytearray.fromhex(src))
        self.dst = bytes(bytearray.fromhex(dst))
        self.type = bytes(bytearray.fromhex("0800"))
        self.listenType = socket.htons(257)
        self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
        self.listenSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
        self.frame = {}
        self.socket.bind(("eth0", 2))
        self.listenSocket.bind(("eth0", 2))
        print("Socket: " + str(self.socket))

        self.device = build_device()  #from build_input header file
        self.config = build_config(self.device) #from build_input header file
        self.state = build_state(self.device, self.config)   #from build_input header file


        self.payload =  encode_state(self.state) #from appcodec header file

    @asyncio.coroutine
    def poll(self):
        while True:
            events = yield from self.device.async_read()
            for event in events:
                if event.type == evdev.ecodes.EV_KEY or event.type ==evdev.ecodes.EV_ABS:
                    self.update_state(event)
        print (self.state)


    def update_state(self, event):
        """mannaged by poll()"""
        self.state[self.config[event.code]] = event.value
        self.pack_state()

    def pack_state(self):
        """mannaged by update_state"""
        self.payload = encode_state(self.state) #from header appcodec header file

    @asyncio.coroutine
    def send(self):
        while True:
            assert(len(self.src) == len(self.dst) == 6)
            assert(len(self.type) == 2)
            self.socket.send(self.dst + self.src + self.type + self.payload)
            yield from asyncio.sleep(.01)

    def run_send_app(self):
        asyncio.async(self.send())
        asyncio.async(self.poll())

        loop = asyncio.get_event_loop()
        loop.run_forever()

    @asyncio.coroutine
    def listen(self):
        while True:
            holder = self.listenSocket.recv(2040)
            if self.frame != holder:
                self.state = decode_packet(self.frame)

            yield from asyncio.sleep(.01)

    @asyncio.coroutine
    def print_packet(self):
        while True:
            print(self.state)
            yield from asyncio.sleep(.01)


    def run_recieve_app(self):
        asyncio.async(self.listen())
        asyncio.async(self.print_packet())

        loop = asyncio.get_event_loop()
        loop.run_forever()
