#!/usr/bin/python

import serial
import time

ser = serial.Serial("/dev/ttyS0", 115200)


def execute(command):
    print("executing command: "+command)
    command += '\r\n'
    ser.write(command.encode('iso-8859-1'))
    time.sleep(0.05)
    data = ser.read(ser.inWaiting()).decode('iso-8859-1')
    print('got response: '+data)
    return data

execute('AT+CGNSPWR?')
execute('AT+CGATT?')
execute('AT+CSTT?')
execute('AT+CIFSR')
execute('AT+CIPSTATUS')

