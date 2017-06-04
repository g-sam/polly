"""
Reply format. See http://cl.ly/ekot

0 Header   '\xaa'
1 Command  '\xc0'
2 DATA1    PM2.5 Low byte
3 DATA2    PM2.5 High byte
4 DATA3    PM10 Low byte
5 DATA4    PM10 High byte
6 DATA5    ID byte 1
7 DATA6    ID byte 2
8 Checksum Low byte of sum of DATA bytes
9 Tail     '\xab'

"""

import machine
import ustruct as struct
import mqtt
import sys
import utime as time

uart = machine.UART(0, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

def wake():
    global uart
    while uart.read(1) == None:
        print('Sending wake command to sds011')
        cmd = b'\xaa\xb4\x06\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x06\xab'
        uart.write(cmd)
    print('sds011 woke up!')

def sleep():
    global uart
    AWAKE = True
    while AWAKE:
        print('Sending sleep command to sds011')
        cmd = b'\xaa\xb4\x06\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x05\xab'
        uart.write(cmd)
        header = uart.read(1)
        if header == b'\xaa':
            command = uart.read(1)
            if command == b'\xc5':
                AWAKE = False
    print('sds011 successfully put to sleep')

def process_packet(packet):
    try:
        print('\nPacket:', packet)
        *data, checksum, tail = struct.unpack('<HHBBBs', packet)
        pm25 = data[0]/10.0
        pm10 = data[1]/10.0
        # device_id = str(data[2]) + str(data[3])
        checksum_OK = checksum == (sum(data) % 256)
        tail_OK = tail == b'\xab'
        packet_status = 'OK' if (checksum_OK and tail_OK) else 'NOK'
        print('PM 2.5:', pm25, '\nPM 10:', pm10, '\nStatus:', packet_status)
        mqtt.publish({
            'pm25': pm25,
            'pm10': pm10,
            'status': packet_status
        })
    except Exception as e:
        print('Problem decoding packet:', e)
        sys.print_exception(e)

def read(allowed_time):
    global uart
    print('Reading from sds011 for', (allowed_time / 1000), 'secs')
    start_time = time.ticks_ms()
    SHOULD_READ = True
    while SHOULD_READ:
        try:
            delta_time = time.ticks_diff(time.ticks_ms(), start_time)
            if (delta_time > allowed_time): SHOULD_READ = False
            header = uart.read(1)
            if header == b'\xaa':
                command = uart.read(1)
                if command == b'\xc0':
                    packet = uart.read(8)
                    process_packet(packet)
        except Exception as e:
            print('Problem attempting to read:', e)
            sys.print_exception(e)
