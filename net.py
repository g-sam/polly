import network
import config
import webrepl
import logging

log = logging.getLogger('net')

def connect():

    file = open('data.txt')
    [ssid, pw] = file.read().strip().split('\n')
    file.close()

    ap_if = network.WLAN(network.AP_IF)
    ap_if.config(essid=config.essid, password=pw)
    log.debug('access point Polly open')

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        log.debug('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pw)
        while not sta_if.isconnected():
            pass
    log.debug('connected at: %s', sta_if.ifconfig())

    if (config.DEBUG):
        webrepl.start()

