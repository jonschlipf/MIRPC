from abc import ABC, abstractmethod
import time
import pyvisa as visa
class Stage(ABC):
    @abstractmethod
    def get_name(self):
        pass

class C863(Stage):
    def __init__(self,instr,bus_address,minpos,maxpos):
        self.instr=instr
        self.maxpos=maxpos
        self.minpos=minpos
        if bus_address==1: #only one implemented
            self.instr.write_raw(b'\x01\x31') #default bus address is 0
        else:
            self.instr.write_raw(b'\x01\x30') #default bus address is 0
    def get_name(self):
        return self.instr.query("VE\r")
    def go_low(self):
        print("finding stage home")
        self.instr.write("MN\r")
        time.sleep(1)
        self.instr.write('FE1\r')
        time.sleep(5)
        self.instr.write('DH\r')
        print("stage home found")

    def get_status(self):
        return self.instr.query("TS\r")
    def set_drive_status(self,target:bool):
        if target:
            self.instr.write("MN\r")
        else:
            self.instr.write("MF\r")
    def set_position(self,target:int):
        if (target<=self.maxpos) and (target>=self.minpos):
            self.instr.write(f"MA{str(target)}\r")
        else:
            print("out of range")
    def get_position(self):
        return self.instr.query("TP\r")

def find_xstage(rm):
    res=rm.list_resources()
    numres=len(res)
    for i in range(0,numres):
        try:
            inst=rm.open_resource(res[i])
            inst.write_raw(b'\x01\x30')
            inst.query("VE\r")
            print("x stage found at "+rm.list_resources()[i])
            return i
        except:
            pass
    print("no x stage found")
    return 0
def find_zstage(rm):
    res=rm.list_resources()
    numres=len(res)
    for i in range(0,numres):
        try:
            inst=rm.open_resource(res[i])
            inst.write_raw(b'\x01\x31')
            inst.query("VE\r")
            print("z stage found at "+rm.list_resources()[i])
            return i
        except:
            pass
    print("no z stage found")
    return 0
def find_ystage(rm):
    res=rm.list_resources()
    numres=len(res)
    for i in range(0,numres):
        try:
            inst=rm.open_resource(res[i])
            inst.query("2 *IDN?\n")
            print("y stage found at "+rm.list_resources()[i])
            return i
        except:
            pass
    print("no y stage found")
    return 0

class C867(Stage):
    def __init__(self,instr,bus_address):
        self.instr=instr
        self.instr.write("2 RON 1 1\n")
        self.instr.write("2 SVO 1 1\n")
        self.instr.write("2 FRF\n")
        time.sleep(1)
    def get_name(self):
        self.instr.query("2 *IDN?\n")
    def set_drive_status(self,target:bool):
        if target:
            self.instr.write("2 SVO 1 1\n")
        else:
            self.instr.write("2 SVO 1 0\n")
    def set_position(self,target:float): #may use MVR(relative pos
        #self.instr.write(f"2 FRF\n")
        self.instr.write(f"2 MOV 1 {str(target)}\n")
    def get_position(self):
        return self.instr.query("2 POS?\n")

class Stage3():
    def __init__(self):
        self.rm=visa.ResourceManager()
        xstage_instr=self.rm.list_resources()[find_xstage(self.rm)] 
        ystage_instr=self.rm.list_resources()[find_ystage(self.rm)]
        zstage_instr=self.rm.list_resources()[find_zstage(self.rm)]
        self.xstage=C863(self.rm.open_resource(xstage_instr),0,00000,275000)
        self.xstage.go_low()
        self.ystage=C867(self.rm.open_resource(ystage_instr),0)
        self.zstage=C863(self.rm.open_resource(zstage_instr),1,100000,270000)
        self.xstage.set_drive_status(1)
        self.ystage.set_drive_status(1)
        self.zstage.set_drive_status(1)
    def set_pos_mm(self,x,y,z):
        self.xstage.set_position(int(round((x+0)*10**4)))
        self.ystage.set_position(y)
        self.zstage.set_position(int(round(z*2*10**3)+100000))

    def get_pos_mm(self):
        xp=float(self.xstage.get_position()[3:])/(10**4)
        yp=float(self.ystage.get_position()[6:])
        zp=(float(self.zstage.get_position()[3:])-100000)/(2*10**3)
        return [xp,yp,zp]
