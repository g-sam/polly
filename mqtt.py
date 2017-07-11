from umqtt.robust import MQTTClient
import ujson as json
import logging
import config

log = logging.getLogger('mqtt')

MQTT_CONFIG = config.MQTT_CONFIG

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
