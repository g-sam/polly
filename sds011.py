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

CMDS = {'SET': b'\x01',
        'GET': b'\x00',
        'DUTYCYCLE': b'\x08',
        'SLEEPWAKE': b'\x06'}

def make_command(cmd, mode, param):
    header = b'\xaa\xb4'
    padding = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff'
    checksum = chr(( ord(cmd) + ord(mode) + ord(param) + 255 + 255) % 256)
    tail = b'\xab'
    return header + cmd + mode + param + padding + bytes(checksum, 'utf8') + tail

def confirm_response(confirmation):
    if (uart.read(1) == b'\xaa'):
        if (uart.read(1) == b'\xc5'):
            print(confirmation)

# sensor wakes for 60 secs before issuing measurment
def set_dutycycle(rest_mins):
    global uart
    cmd = make_command(CMDS['DUTYCYCLE'], CMDS['SET'], chr(rest_mins))
    print('Setting sds011 to read every', rest_mins, 'minutes:', cmd)
    uart.write(cmd)
    time.sleep_ms(1000)
    read(2)

def wake():
    global uart
    cmd = make_command(CMDS['SLEEPWAKE'], CMDS['SET'], chr(1))
    print('Sending wake command to sds011:', cmd)
    uart.write(cmd)
    time.sleep_ms(12000)
    read(2)

def sleep():
    global uart
    cmd = make_command(CMDS['SLEEPWAKE'], CMDS['SET'], chr(0))
    print('Sending sleep command to sds011:', cmd)
    uart.write(cmd)
    time.sleep_ms(2000)

def process_reply(packet):
    print('Reply received:', packet)

def process_measurement(packet):
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

def read(allowed_time=0):
    global uart
    start_time = time.ticks_ms()
    delta_time = 0
    while (delta_time <= allowed_time * 1000):
        try:
            header = uart.read(1)
            if header == b'\xaa':
                command = uart.read(1)
                if command == b'\xc0':
                    packet = uart.read(8)
                    process_measurement(packet)
                elif command == b'\xc5':
                    packet = uart.read(8)
                    process_reply(packet)
            delta_time = time.ticks_diff(time.ticks_ms(), start_time) if allowed_time else 0
        except Exception as e:
            print('Problem attempting to read:', e)
            sys.print_exception(e)
