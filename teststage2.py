import stages as sta
import pyvisa as visa
import time

rm=visa.ResourceManager()
print(rm.list_resources())
xstage_instr=rm.list_resources()[sta.find_xstage(rm)]
ystage_instr=rm.list_resources()[sta.find_ystage(rm)]
zstage_instr=rm.list_resources()[sta.find_zstage(rm)]
#zstage_instr=rm.list_resources()[sta.find_zstage(rm)]
xstage=sta.C863(rm.open_resource(xstage_instr),0,0,275000)
xstage.go_low()
ystage=sta.C867(rm.open_resource(ystage_instr),0)
zstage=sta.C863(rm.open_resource(zstage_instr),1,100000,500000)
#zstage.go_low()
print(xstage.get_name())
print(ystage.get_name())
print(zstage.get_name())
print(xstage.get_status())
print(zstage.get_status())
#time.sleep(10)
xstage.set_drive_status(1)
ystage.set_drive_status(1)
zstage.set_drive_status(1)
#time.sleep(10)
print(xstage.get_position())
print(ystage.get_position())
print(zstage.get_position())
xstage.set_position(200000) #2 cm = 200000 * 100nm
ystage.set_position(47.3)
zstage.set_position(30000) #1.5 cm = 30000 * 500nm
time.sleep(10)
print(xstage.get_position())
print(ystage.get_position())
print(zstage.get_position())
ystage.set_position(0)
xstage.set_position(0)
zstage.set_position(130000)
#time.sleep(10)
#xstage.set_drive_status(0)
#ystage.set_drive_status(0)
#zstage.set_drive_status(0)

