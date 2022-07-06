import usb.core
import usb.util
import time
import struct

BM_REQUEST_TYPE = 0xB3
B_REQUEST_OUT = 0x40
B_REQUEST_IN = 0xC0

#class for controliing the horiba ihr320 monochromator
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
        #wait until done
        while self.busy_filter() or self.busy_grating() or self.busy_144():
            print("Initializing monochromator")
            time.sleep(1)
        #check current wavelength and grating
        self.wavelength=self._get_wavelength_int()
        self.grating=self._get_grating_int()
        self.filter=self._get_filter_int()
        print("Monochromator ready")

    #this uses internal methods to access the hardware and variables to save the hardware state
    def _get_grating_int(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x0, 16, 4)
        return int.from_bytes(g,byteorder='little')
    def set_grating(self,g):
        g=g%3 #make sure it stays in range
        #get a wavelength to come back
        temp_wl=self.get_wavelength()
        #while the grating is not the desired one
        while self._get_grating_int()!=g:
            print("setting grating")
            self.dev.ctrl_transfer(B_REQUEST_OUT, BM_REQUEST_TYPE, 0x0, 17, struct.pack("<i", g))
            #wait while busy
            while self.busy_grating():
                time.sleep(1)
            time.sleep(1)
        #set wavelength again
#        self.set_wavelength(temp_wl)
        #update grating info
        self.grating=self._get_grating_int()
    def get_grating(self):
            return self.grating
    #query if the grating turred is busy
    def busy_grating(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x0, 5, 4)
        return bytearray(g)==bytearray(b'\x01\x00\x00\x00')
    #get the current filter
    def get_filter(self):
        return self.filter
    def _get_filter_int(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x0, 19, 4)
        return int.from_bytes(g,byteorder='little')
    def busy_filter(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x0, 21, 4)
        return bytearray(g)==bytearray(b'\x01\x00\x00\x00')
    def set_filter(self,g):
        g=g%7 #make sure it stays in range
        self.filter=g
        if g>0:
            self._set_filter_int(g)
        else:
            self.auto_filter()
    #automatically selects appropriate filter based on wavelength
    def auto_filter(self):
        if self.filter==0:
            if self.wavelength<1100:
                self._set_filter_int(1)
            elif self.wavelength<2000:
                self._set_filter_int(2)
            elif self.wavelength<3600:
                self._set_filter_int(3)
            else:
                self._set_filter_int(4)

    def _set_filter_int(self,g):
        #prevent theoretically unreachable issue
        if g==0:
            g=6
        #wait until matches target
        while self._get_filter_int()!=g:
            print("move filter wheel")
            self.dev.ctrl_transfer(B_REQUEST_OUT, BM_REQUEST_TYPE, 0x0, 20, struct.pack("<i", g))
            #wait while busy
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
    #set entry slit width
    def set_entr_slit(self,width):
        #prevent overrange
        if width<0:
            width=0
        if width>30:
            width=30
        #wait until value is close to target
        while abs(width-self.get_entr_slit())>.01:
            #calibration constant
            const=7/1000
            #set slit
            self.dev.ctrl_transfer(B_REQUEST_OUT, BM_REQUEST_TYPE, 0x0, 33, struct.pack("<i", round(width / const)))
            time.sleep(.01)
            #wait while busy
            while (self.busy_grating() or self.busy_144()):
                time.sleep(.01)
    def get_exit_slit(self):
        g=self.dev.ctrl_transfer(B_REQUEST_IN, BM_REQUEST_TYPE, 0x02, 32, 4)
        return int.from_bytes(g,byteorder='little')*7/1000
    #see entrance slit
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
        #prevent overrange
        if (wl0<0) or (wl0>1580 * 1200 /(150*2**self._get_grating_int())):
            wl0=0
        #while target not reached
        while abs(wl0-self._get_wavelength_int())>.001*wl0:
            #compute value to send
            wl=wl0*(150*2**self._get_grating_int())/1200
            #set wl 
            self.dev.ctrl_transfer(B_REQUEST_OUT, BM_REQUEST_TYPE, 0x00, 4, struct.pack("<f", wl))
            time.sleep(.01)
            #wait until done
            while (self.busy_grating() or self.busy_144()):
                time.sleep(.01)
        self.wavelength=self._get_wavelength_int()
        self.auto_filter()
    def get_wavelength(self):
        return self.wavelength

