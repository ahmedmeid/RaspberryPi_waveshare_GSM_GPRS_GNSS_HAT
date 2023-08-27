#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

GPIO.output(7, GPIO.LOW)
time.sleep(4)
GPIO.output(7, GPIO.HIGH)
GPIO.cleanup()

time.sleep(3)

ser = serial.Serial("/dev/ttyS0", 115200)


def execute(command):
    print("executing command: "+command)
    command += '\r\n'
    ser.write(command.encode('iso-8859-1'))
    time.sleep(0.05)
    data = ser.read(ser.inWaiting()).decode('iso-8859-1')
    print('got response: '+data)
    return data


execute('AT+CGNSPWR=1')
execute('AT+CGATT=1')
time.sleep(7)
execute('AT+CSTT="JAWALNET.COM.SA"')
execute('AT+CIICR')

