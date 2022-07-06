from abc import ABC, abstractmethod
import time
import pyvisa as visa
class Stage(ABC):
    @abstractmethod
    def get_name(self):
        pass

#C863 stage (used for x and z axis)
class C863(Stage):
    #create stage object
    def __init__(self,instr,bus_address,maxpos):
        #handle of visa instrument and position hard limit
        self.instr=instr
        self.maxpos=maxpos
        #distinguish by PI bus address
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
        #motor on
        self.instr.write("MN\r")
        time.sleep(1)
        #find lower edge
        self.instr.write('FE1\r')
        time.sleep(5)
        self.instr.write('DH\r')
    #go to center of range
    def go_center(self):
        print("finding stage home at center")
        #motor on
        self.instr.write("MN\r")
        self.instr.write("BF\r")
        time.sleep(1)
        #move forward
        self.instr.write(f"MA20000\r")
        time.sleep(5)
        #find edge
        self.instr.write('FE2\r')
        time.sleep(5)
        self.instr.write('DH\r')

    #read status byte
    def get_status(self):
        return self.instr.query("TS\r")
    #switch drive servo on and off
    def set_drive_status(self,target:bool):
        if target:
            self.instr.write("MN\r")
        else:
            self.instr.write("MF\r")
    #set the position of the stage
    def set_position(self,target:int):
        #check (soft) limits
        if (target<=self.maxpos) and (target>=0):
            self.instr.write(f"MA{str(target)}\r")
        else:
            print("out of range")
    #get the position of the stage
    def get_position(self):
        return self.instr.query("TP\r")
    #check if stage is where it should be
    def on_target(self):
        #can have errors, so see if you get the position
        try:
            posval=int(self.instr.query("TE\r")[3:])
        except:
            posval=0
        return posval<10

#finds the stage assigned to the x axis
def find_xstage(rm):
    #get all pyvisa devices
    res=rm.list_resources()
    numres=len(res)
    #loop through device
    for i in range(0,numres):
        try:
            #establish communications
            inst=rm.open_resource(res[i])
            #select device address
            inst.write_raw(b'\x01\x30')
            #see if device responds (no response leads to error)
            inst.query("VE\r")
            print("x stage found at "+rm.list_resources()[i])
            return i
        except:
            pass
    print("no x stage found")
    return 0
#finds the stage assigned to the z axis, see above
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
#finds the stage assigned to the y axis
def find_ystage(rm):
    res=rm.list_resources()
    numres=len(res)
    for i in range(0,numres):
        try:
            inst=rm.open_resource(res[i])
            #check if responds
            inst.query("2 *IDN?\n")
            print("y stage found at "+rm.list_resources()[i])
            return i
        except:
            pass
    print("no y stage found")
    return 0

#C867 stage (used for y axis)
class C867(Stage):
    def __init__(self,instr,bus_address):
        self.instr=instr
        #switch on
        self.instr.write("2 RON 1 1\n")
        #switch servo on
        self.instr.write("2 SVO 1 1\n")
        #set to reference (center) position
        self.instr.write("2 FRF\n")
        time.sleep(1)
    #get stage id
    def get_name(self):
        self.instr.query("2 *IDN?\n")
    #switch servo on and off
    def set_drive_status(self,target:bool):
        if target:
            self.instr.write("2 SVO 1 1\n")
        else:
            self.instr.write("2 SVO 1 0\n")
    #set position of servo
    def set_position(self,target:float): #may use MVR(relative pos
        self.instr.write(f"2 MOV 1 {str(target)}\n")
    #get position of servo
    def get_position(self):
        return self.instr.query("2 POS?\n")
    #get target position
    def get_target(self):
        return self.instr.query("2 MOV?\n")
    #see if the stage is close to target
    def on_target(self):
        return abs(float(self.get_position()[6:])-float(self.get_target()[6:]))<0.01

#object describing all 3 stages
class Stage3():
    def __init__(self):
        self.rm=visa.ResourceManager()
        #find all three stages
        xstage_instr=self.rm.list_resources()[find_xstage(self.rm)] 
        ystage_instr=self.rm.list_resources()[find_ystage(self.rm)]
        zstage_instr=self.rm.list_resources()[find_zstage(self.rm)]
        #make objects for stage control
        self.xstage=C863(self.rm.open_resource(xstage_instr),0,275000)
        #x stage starts at low limit
        self.xstage.go_low()
        self.ystage=C867(self.rm.open_resource(ystage_instr),0)
        self.zstage=C863(self.rm.open_resource(zstage_instr),1,500000)
        #z stage starts at center
        self.zstage.go_center()
        #make sure all drives are on
        self.xstage.set_drive_status(1)
        self.ystage.set_drive_status(1)
        self.zstage.set_drive_status(1)
    #set x,y,and z coordinate in mm
    def set_pos_mm(self,x,y,z):
        self.xstage.set_position(int(round((x+0)*10**4)))
        self.ystage.set_position(y)
        self.zstage.set_position(int(round(z*2*10**3)))
        #if z needs time, wait
        if abs(float(self.zstage.get_position()[3:])/(2*10**3)-z)>1:
            time.sleep(3)

        for i in range(0,1000):
            #wait until timeout (100s), or until x and y are on target
            time.sleep(.1)
            if self.xstage.on_target() & self.ystage.on_target():
                break
    #get positions of all 3 stages
    def get_pos_mm(self):
        xp=float(self.xstage.get_position()[3:])/(10**4)-0
        yp=float(self.ystage.get_position()[6:])
        zp=float(self.zstage.get_position()[3:])/(2*10**3)
        return [xp,yp,zp]
