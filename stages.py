from abc import ABC, abstractmethod
import pyvisa as visa
class Stage(ABC):
    @abstractmethod
    def get_name(self):
        pass

class C863(Stage):
    def __init__(self,instr,bus_address):
        self.instr=instr
        self.instr.write_raw(b'\x01\x30') #default bus address is 1
    def get_name(self):
        return self.instr.query("VE\r")
    def set_drive_status(self,target:bool):
        if target:
            self.instr.write("MN\r")
        else:
            self.instr.write("MF\r")
    def set_position(self,target:int):
        self.instr.write(f"MA{str(target)}\r")
    def get_position(self):
        return self.instr.query("TP\r")

class C867(Stage):
    def __init__(self,instr,bus_address):
        self.instr=instr
        self.instr.write("2 ron 1 1\n")
    def get_name(self):
        stage.query("?idn\n")
    def set_drive_status(self,target:bool):
        if target:
            self.instr.write("2 svo 1 1\n")
        else:
            self.instr.write("2 svo 1 0\n")
    def set_position(self,target:int): #may use MVR(relative pos
        self.instr.write(f"mov{str(int)}\n")
    def get_position(self):
        return self.instr.query("pos?\n")

