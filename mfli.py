#import time
import zhinst.ziPython as zi
import math
class MFLI():
    def __init__(self):
        discovery = zi.ziDiscovery()
        device_id = discovery.find('MF-DEV5880')
        device_props = discovery.get(device_id)
        self.daq = zi.ziDAQServer(device_props['serveraddress'], device_props['serverport'], device_props['apilevel'])
        self.scope = self.daq.scopeModule()
        self.daq.setInt('/dev5880/auxouts/2/demodselect', 0)
        self.daq.setInt('/dev5880/auxouts/2/demodselect', 0)
        self.daq.setInt('/dev5880/auxouts/3/demodselect', 0)
        self.daq.setInt('/dev5880/auxouts/3/demodselect', 0)
        self.scope.set('lastreplace', 1)
        self.scope.set('averager/weight', 1)
        self.scope.set('averager/restart', 0)
        self.scope.set('averager/weight', 1)
        self.scope.set('averager/restart', 0)
        self.scope.set('fft/power', 0)
        self.scope.set('mode', 1)
        self.scope.set('fft/spectraldensity', 0)
        self.scope.set('fft/window', 1)
        self.scope.set('save/directory', '/data/LabOne/WebServer')
        self.daq.setInt('/dev5880/auxouts/3/outputselect', -1)#use aux3 as bias, set to -1
        self.daq.setDouble('/dev5880/oscs/0/freq', 5.67)
    #set oscillator frequency in Hz
    def set_oscillator(self,freq):
        self.daq.setDouble('/dev5880/oscs/0/freq', freq)
        if freq>10:
            self.daq.setInt('/dev5880/demods/0/sinc', 1)
        else:
            self.daq.setInt('/dev5880/demods/0/sinc', 0)
    def get_oscillator(self):
        return self.daq.getDouble('/dev5880/oscs/0/freq')
    #set oscillator output on/off
    def set_sigout_on(self,val):
        self.daq.setInt('/dev5880/sigouts/0/on', val)
    def get_sigout_on(self):
        return self.daq.getInt('/dev5880/sigouts/0/on')
    #set lockin harmonic
    def set_harmonic(self,harm):
        self.daq.setDouble('/dev5880/demods/0/harmonic', harm)
    def get_harmonic(self):
        return self.daq.getDouble('/dev5880/demods/0/harmonic')
    #set lockin lpf order
    def set_order(self,order):
        self.daq.setInt('/dev5880/demods/0/order', order)
    def get_order(self):
        return self.daq.getInt('/dev5880/demods/0/order')
    #set lockin lpf time constant
    def set_timeconst(self,tc):
        self.daq.setDouble('/dev5880/demods/0/timeconstant', tc)
    def get_timeconst(self):
        return self.daq.getDouble('/dev5880/demods/0/timeconstant')
    #set lockin current input
    def set_input(self,inp):
        self.daq.setInt('/dev5880/demods/0/adcselect', inp)
    def get_input(self):
        return self.daq.getInt('/dev5880/demods/0/adcselect')
    #set lockin current input range
    def set_input_current_range(self,rng):
        self.daq.setDouble('/dev5880/currins/0/range', rng)
    def auto_input_current_range(self):
        self.daq.setInt('/dev5880/currins/0/autorange', 1)
    def get_input_current_range(self):
        return self.daq.getDouble('/dev5880/currins/0/range')
    #set lockin voltage input range
    def set_input_voltage_range(self,rng):
        self.daq.setDouble('/dev5880/sigins/0/range', rng)
    def auto_input_voltage_range(self):
        self.daq.setInt('/dev5880/sigins/0/autorange', 1)
    def get_input_voltage_range(self):
        return self.daq.getDouble('/dev5880/sigins/0/range')
    #set lockin voltage output range
    def set_output_voltage_range(self,rng):
        self.daq.setDouble('/dev5880/sigouts/0/range', rng)
    def get_output_voltage_range(self):
        return self.daq.getDouble('/dev5880/sigouts/0/range')
    #set lockin voltage output amplitude
    def set_output_amplitude(self,amp):
        self.daq.setDouble('/dev5880/sigouts/0/amplitudes/1', amp)
    def get_output_amplitude(self):
        return self.daq.getDouble('/dev5880/sigouts/0/amplitudes/1')
    #set aux4 as voltage bias for the DUT
    def set_bias(self,vbias):
        self.daq.setDouble('/dev5880/auxouts/3/offset', vbias)
    def get_bias(self):
        return self.daq.getDouble('/dev5880/auxouts/3/offset')
    #retrieve measured lock-in data
    def get_Sample(self):
        return self.daq.getSample('/dev5880/demods/0/sample')
    def get_R(self):
        s=self.get_Sample()
        return math.sqrt(s["x"][0]**2+s["y"][0]**2)
    def get_phi(self):
        s=self.get_Sample()
        return math.atan(s["y"][0]/s["x"][0])*180/math.pi
    def get_Y(self):
        s=self.get_Sample()
        return s["y"][0]

       
