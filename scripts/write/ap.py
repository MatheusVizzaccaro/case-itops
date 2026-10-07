import psutil
import random
import json
import datetime

data = {
    'id_antena': random.randint(0,10),
    'bytes_sent': psutil.net_io_counters().bytes_sent,
    'bytes_recv': psutil.net_io_counters().bytes_recv,
    'active_conn': random.randint(5,50),
    'cpu_usage': psutil.cpu_percent(),
    'ram_usage': psutil.virtual_memory().percent
}

date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')

with open(f'bronze-data/ap01_{date}.json', 'w') as file:
    json.dump(data, file, indent=2)