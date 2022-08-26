from datetime import datetime
from paho import mqtt
import paho.mqtt.client as paho
import time
import random
import json


def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("random210", "Random@210")
client.connect("2f65330fdf214827aa97b8303ee66b94.s1.eu.hivemq.cloud", 8883)
client.on_publish = on_publish

while True:
    payload = {
        "time": datetime.now().replace(microsecond=0).isoformat(),
        "value": round(random.uniform(1000.0, 4000.0), 2),
        "unit": "V"
    }
    time.sleep(random.uniform(0.3, 1))
    # time.sleep(1)
    client.publish(topic="measurements", payload=json.dumps(payload))

if __name__ == '__main__':
    pass
