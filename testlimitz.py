import stages as sta
import time
mystage=sta.Stage3()
time.sleep(1)
mystage.zstage.set_drive_status(1)
time.sleep(1)
print(mystage.zstage.get_status())
mystage.zstage.instr.write('FE3\r')
time.sleep(1)
print(mystage.zstage.get_status())
print(mystage.xstage.get_status())
mystage.zstage.set_drive_status(1)
mystage.xstage.set_drive_status(1)
#while 1==1:
#    print(mystage.zstage.get_status())
#
#    time.sleep(1)
