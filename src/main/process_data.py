import time
import json
import paho.mqtt.client as paho
from paho import mqtt
from statistics import median, mean
import store_data
import pandas as pd
import sys

# host="host.docker.internal"
# default, localhost

connection = store_data.Connection(host="host.docker.internal")


def measuring_data():
    period_start_list = []
    period_end_list = []
    n_list = []
    n_list.extend(range(1, len(times) + 1))
    min_list = []
    max_list = []
    median_list = []
    average_list = []

    for m_time in times:
        period_start_list.append(m_time[0])
        period_end_list.append(m_time[-1])

    for m_value in values:
        min_list.append(min(m_value))
        max_list.append(max(m_value))
        median_list.append(round(median(m_value), 2))
        average_list.append(round(mean(m_value), 2))

    data_frame = pd.DataFrame({"period_start": period_start_list,
                               "period_end": period_end_list,
                               "N": n_list,
                               "min": min_list,
                               "max": max_list,
                               "median": median_list,
                               "average": average_list})
    print(data_frame)
    return data_frame


def convert_data(data):
    global values
    if counter in range(0, number_of_measurement):
        data_decode = str(data.payload.decode("utf-8", "ignore"))
        data_json = json.loads(data_decode)
        print("message: ", data_json)
        values[counter].append(data_json["value"])
        times[counter].append(data_json["time"])


def on_connect(client, userdata, flags, rc, properties=None):
    client.subscribe("measurements/#", qos=1)


def on_message(client, userdata, data):
    convert_data(data)


def run():
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("random210", "Random@210")
    client.connect("2f65330fdf214827aa97b8303ee66b94.s1.eu.hivemq.cloud", 8883)
    client.on_message = on_message

    global counter
    client.loop_start()
    time.sleep(2)
    counter = 0

    for i in range(number_of_measurement):
        print("measurement: ", counter + 1)
        time.sleep(time_interval)
        counter += 1

    client.loop_stop()

    saving_to_database(measuring_data())


def saving_to_database(data_to_save):
    connection.insert_data(data_to_save)
    connection.close_connection()


if __name__ == '__main__':
    global time_interval, number_of_measurement, values, times

    time_interval = int(sys.argv[1])
    number_of_measurement = int(sys.argv[2])

    values = [[] for x in range(number_of_measurement)]
    times = [[] for x in range(number_of_measurement)]
    counter = -1

    run()
