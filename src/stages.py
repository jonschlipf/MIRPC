from abc import ABC, abstractmethod
import time
import pyvisa as visa
class Stage(ABC):
    @abstractmethod
    def get_name(self):
        pass

class C863(Stage):
    #create stage object
    def __init__(self,instr,bus_address,maxpos):
        self.instr=instr
        self.maxpos=maxpos
        if bus_address==1: #only 0 and 1 implemented
            self.instr.write_raw(b'\x01\x31') 
        else:
            self.instr.write_raw(b'\x01\x30') #default bus address is 0
        print(self.on_target())
    #get name of stage
    def get_name(self):
        return self.instr.query("VE\r")
    #go to low limit
    def go_low(self):
        print("finding stage home at low end")
        self.instr.write("MN\r")
        time.sleep(1)
        self.instr.write('FE1\r')
        time.sleep(5)
        self.instr.write('DH\r')
    #go to center of range
    def go_center(self):
        print("finding stage home at center")
        self.instr.write("MN\r")
        self.instr.write("BF\r")
        time.sleep(1)
        self.instr.write(f"MA80000\r")
        time.sleep(5)
        self.instr.write('FE2\r')
        time.sleep(5)
        self.instr.write('DH\r')

    def get_status(self):
        return self.instr.query("TS\r")
    def set_drive_status(self,target:bool):
        if target:
            self.instr.write("MN\r")
        else:
            self.instr.write("MF\r")
    def set_position(self,target:int):
        if (target<=self.maxpos) and (target>=0):
            self.instr.write(f"MA{str(target)}\r")
        else:
            print("out of range")
    def get_position(self):
        return self.instr.query("TP\r")
    def on_target(self):
        try:
            posval=int(self.instr.query("TE\r")[3:])
        except:
            posval=0
        return posval<10


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
    def get_target(self):
        return self.instr.query("2 MOV?\n")
    def on_target(self):
        return abs(float(self.get_position()[6:])-float(self.get_target()[6:]))<0.01

class Stage3():
    def __init__(self):
        self.rm=visa.ResourceManager()
        xstage_instr=self.rm.list_resources()[find_xstage(self.rm)] 
        ystage_instr=self.rm.list_resources()[find_ystage(self.rm)]
        zstage_instr=self.rm.list_resources()[find_zstage(self.rm)]
        self.xstage=C863(self.rm.open_resource(xstage_instr),0,275000)
        self.xstage.go_low()
        self.ystage=C867(self.rm.open_resource(ystage_instr),0)
        self.zstage=C863(self.rm.open_resource(zstage_instr),1,500000)
        self.zstage.go_center()
        self.xstage.set_drive_status(1)
        self.ystage.set_drive_status(1)
        self.zstage.set_drive_status(1)
    def set_pos_mm(self,x,y,z):
        self.xstage.set_position(int(round((x+0)*10**4)))
        self.ystage.set_position(y)
        self.zstage.set_position(int(round(z*2*10**3)))
        if abs(float(self.zstage.get_position()[3:])/(2*10**3)-z)>1:
            time.sleep(3)

        for i in range(0,1000):
            time.sleep(.1)
            if self.xstage.on_target() & self.ystage.on_target():
                break

    def get_pos_mm(self):
        xp=float(self.xstage.get_position()[3:])/(10**4)-0
        yp=float(self.ystage.get_position()[6:])
        zp=float(self.zstage.get_position()[3:])/(2*10**3)
        return [xp,yp,zp]
