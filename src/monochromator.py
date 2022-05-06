import usb.core
import usb.util
import time
import struct

BM_REQUEST_TYPE = 0xB3
B_REQUEST_OUT = 0x40
B_REQUEST_IN = 0xC0

class Monochromator():
    def __init__(self):

        # find our self.device
        self.dev = usb.core.find(idVendor=0x0c9b, idProduct=0x0101)

        # was it found?
        if self.dev is None:
            raise ValueError('Device not found')

        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        self.dev.set_configuration()
        self.dev.ctrl_transfer(B_REQUEST_IN, 179, 0, 1, 4) 
        bytearray(self.dev.ctrl_transfer(B_REQUEST_IN, 6, 0x302, 27, 512))
        self.dev.ctrl_transfer(B_REQUEST_OUT, BM_REQUEST_TYPE, 0, 0, 0) #init
        while self.busy_filter() or self.busy_grating() or self.busy_144():
            print("Initializing monochromator")
            time.sleep(1)
        self.wavelength=self._get_wavelength_int()
        self.grating=self._get_grating_int()
        print("Monochromator ready")

    def _get_grating_int(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x0, 16, 4)
        return int.from_bytes(g,byteorder='little')
    def set_grating(self,g):
        g=g%3 #make sure it stays in range
        temp_wl=self.get_wavelength()
        while self._get_grating_int()!=g:
            print("setting grating")
            self.dev.ctrl_transfer(B_REQUEST_OUT, BM_REQUEST_TYPE, 0x0, 17, struct.pack("<i", g))
            while self.busy_grating():
                time.sleep(1)
            time.sleep(1)
        self.set_wavelength(temp_wl)
        self.grating=self._get_grating_int()
    def get_grating(self):
            return self.grating
    def busy_grating(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x0, 5, 4)
        return bytearray(g)==bytearray(b'\x01\x00\x00\x00')

    def get_filter(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x0, 19, 4)
        return int.from_bytes(g,byteorder='little')
    def busy_filter(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x0, 21, 4)
        return bytearray(g)==bytearray(b'\x01\x00\x00\x00')
    def set_filter(self,g):
        g=g%7 #make sure it stays in range
        if g==0: #auto filter not yet implemented
            g=6
        #print(g)
        while self.get_filter()!=g:
            #print("move")
            self.dev.ctrl_transfer(B_REQUEST_OUT, BM_REQUEST_TYPE, 0x0, 20, struct.pack("<i", g))
            while self.busy_filter():
                print("setting filter")
                time.sleep(1)
            time.sleep(1)
    def busy_144(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x0, 144, 4)
        return bytearray(g)==bytearray(b'\x01\x00\x00\x00')
    def get_entr_slit(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x0, 32, 4)
        return int.from_bytes(g,byteorder='little')*7/1000
    def set_entr_slit(self,width):
        if width<0:
            width=0
        if width>30:
            width=30
        while abs(width-self.get_entr_slit())>.01:
            const=7/1000
            self.dev.ctrl_transfer(B_REQUEST_OUT, BM_REQUEST_TYPE, 0x0, 33, struct.pack("<i", round(width / const)))
            time.sleep(.01)
            while (self.busy_grating() or self.busy_144()):
                time.sleep(.01)
    def get_exit_slit(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x02, 32, 4)
        return int.from_bytes(g,byteorder='little')*7/1000
    def set_exit_slit(self,width):
        if width<0:
            width=0
        if width>30:
            width=30
        while abs(width-self.get_exit_slit())>.01:
            const=7/1000    
            self.dev.ctrl_transfer(B_REQUEST_OUT, BM_REQUEST_TYPE, 0x02, 33, struct.pack("<i", round(width / const)))
            time.sleep(.01)
            while (self.busy_grating() or self.busy_144()):
                time.sleep(.01)
    def _get_wavelength_int(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x0, 2, 4)
        return struct.unpack('f',g)[0]*1200/(150*2**self._get_grating_int())
    def set_wavelength(self,wl0):
        if (wl0<0) or (wl0>1580 * 1200 /(150*2**self._get_grating_int())):
            wl0=0
        while abs(wl0-self._get_wavelength_int())>.001*wl0:
            wl=wl0*(150*2**self._get_grating_int())/1200
            self.dev.ctrl_transfer(B_REQUEST_OUT, BM_REQUEST_TYPE, 0x00, 4, struct.pack("<f", wl))
            time.sleep(.01)
            while (self.busy_grating() or self.busy_144()):
                time.sleep(.01)
        self.wavelength=self._get_wavelength_int()
    def get_wavelength(self):
        return self.wavelength

