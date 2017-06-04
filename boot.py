# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import utime as time
gc.collect()

print('\nbooting...')

def do_connect():
    import network

    file = open('data.txt')
    pw = file.read().strip()
    file.close()

    ap_if = network.WLAN(network.AP_IF)
    ap_if.config(essid='Polly', password=pw)
    print('access point Polly open')

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Bam-net', pw)
        while not sta_if.isconnected():
            pass
    print('connected at:', sta_if.ifconfig())

do_connect()
webrepl.start()
time.sleep(1)
print('Booted!')

