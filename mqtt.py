from umqtt.robust import MQTTClient
import ubinascii as binascii
import machine
import ujson as json
import logging

log = logging.getLogger('mqtt')

MQTT_CONFIG = { 'broker': '192.168.1.10',
               'client_id': b'polly_' + binascii.hexlify(machine.unique_id()) }

MQTT_CONFIG.update({'topic': b'polly/' + MQTT_CONFIG['client_id']})

client = MQTTClient(MQTT_CONFIG['client_id'], MQTT_CONFIG['broker'])
client.connect()

log.debug('MQTT client connected to broker %s', MQTT_CONFIG['broker'])

def publish(msg):
    global client
    msg.update({
        'client_id': MQTT_CONFIG['client_id']
    })
    client.publish(MQTT_CONFIG['topic'], bytes(json.dumps(msg), 'utf8'))
    log.debug('Message sent to %s on %s', MQTT_CONFIG['broker'], MQTT_CONFIG['topic'])
