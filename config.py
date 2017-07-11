import ubinascii as binascii
import machine

essid = 'Polly'
DEBUG = True
SDS011_INIT_SECONDS = 23
READ_SECONDS = 7
SLEEP_SECONDS = 60

MQTT_CONFIG = { 'broker': '192.168.1.10',
               'client_id': b'polly_' + binascii.hexlify(machine.unique_id()) }

MQTT_CONFIG.update({'topic': b'polly/' + MQTT_CONFIG['client_id']})



