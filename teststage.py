import stages as sta
import pyvisa as visa
import time

rm=visa.ResourceManager()
print(rm.list_resources())
xstage_instr=rm.list_resources()[1]
ystage_instr=rm.list_resources()[3]
zstage_instr=rm.list_resources()[2]
xstage=sta.C863(rm.open_resource(xstage_instr),0)
ystage=sta.C867(rm.open_resource(zstage_instr),0)
zstage=sta.C863(rm.open_resource(zstage_instr),1)
print(xstage.get_name())
#print(ystage.get_name())
print(zstage.get_name())
xstage.set_drive_status(1)
zstage.set_drive_status(1)
print(zstage.get_position())
#xstage.set_position(20000000)
zstage.set_position(20000000)
time.sleep(5)
print(zstage.get_position())
xstage.set_position(0)
zstage.set_position(0)
