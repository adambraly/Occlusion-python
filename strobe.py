######### Adam Braly 12/08/2015 ############
############################################
#                                          #
# Pins on data register  8-bits total      #
#   9   8   7   6   5   4   3   2          #
#                                          #
# Pin 2 is the left  eye (egocentric)      #
# Pin 3 is the right eye (egocentric)      #
#                                          #
# Setting the pin to value 0 will open     #
# Setting the pin to value 1 will close    #
#                                          #
# Example usage: p.Out32(port, byte)       #
# Writes a byte to the specified port      #
# 8 bits in a byte; 1 bit per pin          #
#                                          #
# 0 = 00000000; 1 = 00000001               #
# 2 = 00000010; 3 = 00000011 etc..         #
#                                          #
# 0x01 hexadecimal = 00000001 binary,      #
#   setting the value of pin 2 to 1.       #
#                                          #
# 0x02 hexadecimal = 00000010 binary       #
#   setting the value of pin 3 to 1.       #
#                                          #
# 0x03 hexadecimal = 00000011 binary       #
#   setting the value of pins 2 & 3 to 1.  #
#                                          #
# NOTE: Byte values of 0,1,2,3 are the     #
# easiest to use for this purpose.         #
#     0x00 or 0 = both  lens open          #
#     0x01 or 1 = left  lens close         #
#     0x02 or 2 = right lens close         #
#     0x03 or 3 = both lens  closded       #
# However, larger values can also be used. #
#                                          #
#              Examples:                   #
# 0xFF hex = 255 decimal = 11111111 binary #
# 0x97 hex = 151 decimal = 10010111 binary #
# 0x63 hex = 099 decimal = 01100011 binary #
#   will all close both lens because       #
#   bits 2 and 3 receive a value of 1.     #
#                                          #
############################################
############################################

import pythoncom, pyHook, sys
import threading, time
from time import sleep
from ctypes import windll

p = windll.inpout32
DATA = 0x378 #DATA REGISTER OF LPT1
  

lock = threading.Lock() #MAKE A NEW LOCK OBJECTS
def KeyEventThread(i):
    lock.acquire()
    strobe_on()
    lock.release()

def KeyEventThread2(i):
    lock.acquire()
    windll.winmm.timeEndPeriod(1)
    p.Out32(DATA, 0x03)
    sys.exit()
    lock.release()

def MouseEventThread(i):
    lock.acquire()
    p.Out32(DATA,0x03)
    lock.release()

def strobe_on():
    sleep(.50)
    start = time.time()
    for i in range (0,12):
        p.Out32(DATA, 0x00) #OPEN GOGGLES
        sleep(.100)         #DURATION TO KEEP OPEN
        p.Out32(DATA, 0x03) #CLOSE GOGGLES
        sleep(.150)         #DURATION TO KEEP CLOSED
    p.Out32(DATA,0x00)      #OPEN RIGHT BEFORE THE OBJECT DISAPPEARS
    print time.time()-start


def OnKeyboardEvent(event): 
    if(event.Key=='Space'):
        t = threading.Thread(target=KeyEventThread, args=(1,)) #START KEYBOARD THREAD
        t.start()
        
    if(event.Key=='C'):
        t = threading.Thread(target=KeyEventThread, args=(1,))
        t.start()
        
    if(event.Key=='Escape'):
        t = threading.Thread(target=KeyEventThread2, args=(1,))
        t.start()
        sys.exit()
        
    return True

def OnMouseEvent(event):
    t = threading.Thread(target=MouseEventThread, args=(1,)) #START MOUSE THREAD
    t.start()

    return True
        
hm = pyHook.HookManager()#MAKE A NEW PYHOOK MANAGER
hm.KeyDown = OnKeyboardEvent #KEYPRESS CALLS THE KEYBOARD EVENT
hm.MouseAllButtonsDown = OnMouseEvent #MOUSE CLICK CALLS THE MOUSE EVENT
hm.HookKeyboard() #HOOK THE KEYBOARD
hm.HookMouse() #HOOK THE MOUSE
windll.winmm.timeBeginPeriod(1) #IMPORTANT: SETS THE SYSTEM CLOCK RESOLUTION TO 1 MS
while True:
    pythoncom.PumpMessages() #RUNNING TRUE AND RETURNS GLOBAL INPUT EVENTS




