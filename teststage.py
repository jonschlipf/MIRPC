import stages as sta
import pyvisa as visa
import time

rm=visa.ResourceManager()
print(rm.list_resources())
zstage_instr=rm.list_resources()[0]
zstage=sta.C863(rm.open_resource(zstage_instr),1)
print(zstage.get_name())
zstage.set_drive_status(1)
print(zstage.get_position())
zstage.set_position(20000000)
time.sleep(5)
print(zstage.get_position())
zstage.set_position(0)
