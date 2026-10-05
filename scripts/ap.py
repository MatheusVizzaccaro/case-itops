import psutil
import random
import json
import datetime

id_antena = random.randint(0,10)
bytes_sent_recv = psutil.net_io_counters()
active_conn = random.randint(5,50)
cpu_usage = psutil.cpu_percent()
ram_usage = psutil.virtual_memory()

data = {
    'ID_antena': id_antena,
    'Bytes_Sent/Recv': bytes_sent_recv,
    'Active_conn': active_conn,
    'Cpu_usage': cpu_usage,
    'Ram_usage': ram_usage.percent
}

date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')

with open(f'{date}_ap01.json', 'w') as file:
    json.dump(data, file, indent=2)