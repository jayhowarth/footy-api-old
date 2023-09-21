from pymemcache.client.base import Client
from datetime import datetime
import time

client = Client('localhost')
client.set('api_calls', 0)
client.set('call_time', datetime.now())


def counter_inc():
    api_counter = client.get('api_calls')
    prev_time = client.get('call_time')
    d = prev_time.decode('utf-8')
    current_time = datetime.now()
    delta_time = current_time - datetime.strptime(d, "%Y-%m-%d %H:%M:%S.%f")
    counter_int = int(api_counter)
    if counter_int < 400 or delta_time.seconds > 3600:
        counter_int += 1
        client.set('api_calls', counter_int)
    else:
        time.sleep(3600)
        client.set('api_calls', 0)
        client.set('call_time', datetime.now())


def get_counter():
    api_counter = client.get('api_calls')
    return api_counter
