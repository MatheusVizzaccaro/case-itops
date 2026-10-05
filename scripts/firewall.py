import psutil
import random
import json

def generate_ipv4():
    ip = ""
    n=0
    while n<4:
        ip += f".{random.randint(0,255)}"
        n+=1

    ip = ip[1:len(ip)]
    return ip

data = {
    'active_sessions': random.randint(5,50),
    'dropped_packets': psutil.net_io_counters().dropin,
    'top_blocked_ip': generate_ipv4(),
    'cpu_usage': psutil.cpu_percent(),
    'ram_usage': psutil.virtual_memory().percent,
    'bytes_sent_recv': psutil.net_io_counters()
}

with open('firewall.json', 'w') as file:
    json.dump(data, file, indent=2)