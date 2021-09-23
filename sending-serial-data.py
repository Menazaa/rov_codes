import serial
import time


ard = serial.Serial('COM7', 9600)
def led_on():
    ard.write(b'1')

def led_off():
    ard.write(b'0')

i=0       
while(i<3):  
    time.sleep(1)
    led_on()    
    time.sleep(1)
    led_off()   
    print("done")
    i+=1
ard.close()   


cv2.destroyAllWindows()  


