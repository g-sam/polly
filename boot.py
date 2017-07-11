# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import webrepl
import utime as time
import logging

DEBUG = True
gc.collect()

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
    import esp
    esp.osdebug(None)

log = logging.getLogger('boot')

def do_connect():
    import network

    file = open('data.txt')
    [ssid, pw] = file.read().strip().split('\n')
    file.close()

    ap_if = network.WLAN(network.AP_IF)
    ap_if.config(essid='Polly', password=pw)
    log.debug('access point Polly open')

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        log.debug('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pw)
        while not sta_if.isconnected():
            pass
    log.debug('connected at: %s', sta_if.ifconfig())

do_connect()
webrepl.start()
time.sleep(2)


