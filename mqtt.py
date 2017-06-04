from umqtt.robust import MQTTClient
import ubinascii as binascii
import machine
import ujson as json

MQTT_CONFIG = { 'broker': '192.168.0.3',
               'client_id': b'polly_' + binascii.hexlify(machine.unique_id()) }

MQTT_CONFIG.update({'topic': b'polly/' + MQTT_CONFIG['client_id']})

client = MQTTClient(MQTT_CONFIG['client_id'], MQTT_CONFIG['broker'])
client.connect()

print('MQTT client connected to broker', MQTT_CONFIG['broker'])

def publish(msg):
    global client
    msg.update({
        'client_id': MQTT_CONFIG['client_id']
    })
    client.publish(MQTT_CONFIG['topic'], bytes(json.dumps(msg), 'utf8'))
    print('Message sent to', MQTT_CONFIG['broker'], 'on', MQTT_CONFIG['topic'])
