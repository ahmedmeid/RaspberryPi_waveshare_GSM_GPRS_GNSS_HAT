#!/usr/bin/python

import serial
import time
import json

nmea_mapping = {
    "GNSS run status": "gnss_run_status",
    "Fix status": "fix_status",
    "UTC date & Time": "utc_date_time",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "MSL Altitude": "msl_altitude",
    "Speed Over Ground": "speed_over_ground",
    "Course Over Ground": "course_over_ground",
    "Fix Mode": "fix_mode",
    "Reserved!": "reserved1",
    "HDOP": "hdop",
    "PDOP": "pdop",
    "VDOP": "vdop",
    "Reserved2": "reserved2",
    "GNSS Satellites in View": "gnss_satellites_in_view",
    "GNSS Satellites Used": "gnss_satellites_used",
    "GLONASS Satellites Used": "glonass_satellites_used",
    "Reserved3": "reserved3",
    "C/NO max": "cno_max",
    "HPA": "hpa",
    "VPA": "vpa"
}

# Configure serial connection
ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)

def send_at_command(command, delay=1):
    print("executing command: "+command)
    ser.write((command + '\r\n').encode('iso-8859-1'))
    time.sleep(delay)
    response = ser.read(ser.in_waiting).decode('iso-8859-1')
    print("got response: "+response)
    return response


def extract_nmea(response):
    json_data = {}
    # Find the index of "+CGNSINF:"
    nmea_start_index = response.find("+CGNSINF:")

    # Extract the substring after "+CGNSINF:"
    if nmea_start_index != -1:
       nmea_data = response[nmea_start_index + len("+CGNSINF:"):].strip()

       # Remove "OK" at the end
       nmea_data = nmea_data.replace("OK", "").strip()
       nmea_fields = nmea_data.split(',')
       for nmea_key, json_key in nmea_mapping.items():
           json_data[json_key] = nmea_fields.pop(0)
    return json_data

 
try:

    # Check if connection is up
    # send_at_command('AT+CIFSR')

    response = send_at_command('AT+CGNSINF')

    nmea_json = extract_nmea(response)
    nmea_sentence = json.dumps(nmea_json)
    
    # Start TCP connection

    send_at_command('AT+CIPSTART="TCP","34.207.233.231",5001')

    # Send JSON data
    
    data = 'POST /api/sensors HTTP/1.1\r\n'
    data += 'Host: ec2-34-207-233-231.compute-1.amazonaws.com\r\n'
    data += 'Content-Type: application/json\r\n'
    data += 'Content-Length: '+str(len(nmea_sentence))+'\r\n'  # Adjust length based on your JSON size
    data += '\r\n'
    data += nmea_sentence
    send_at_command(f'AT+CIPSEND={len(data)}')
    ser.write(data.encode())
    time.sleep(1)
    ser.write(chr(0x1A).encode())  # Ctrl+Z to indicate end of data

    # Wait for response
    time.sleep(2)  # Adjust as needed
    response = ser.read(ser.in_waiting).decode()
    print(response)

    # Close TCP connection
    send_at_command('AT+CIPCLOSE')
finally:
    # Clean up and close the serial connection
    ser.close()
