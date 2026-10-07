import datetime
import os
import json
import csv

jsons = sorted(os.listdir("bronze-data/"))

data = {
    "data_registro": [],

    #Dados da antena:
    "ap_id": [],
    "ap_bytes_sent": [],
    "ap_bytes_recv": [],
    "active_conn": [],
    "ap_cpu_usage": [],
    "ap_ram_usage": [],

    #Dados do firewall:
    "active_sessions": [],
    "dropped_packets": [],
    "top_blocked_ip": [],
    "firewall_cpu_usage": [],
    "firewall_ram_usage": [],
    "firewall_bytes_sent": [],
    "firewall_bytes_recv": [],

    #Dados calculados (silver):
    "mbps_sent": [],
    "mbps_recv": [],
    "status": []
}

checkpoint = {}

if os.path.exists("checkpoint.json"):
    with open("checkpoint.json", 'r') as chkpoimt:
        checkpoint = json.load(chkpoimt)
else:
    checkpoint = {
        "ap_last_file": "",
        "firewall_last_file": "",
        "ap_sent": 0,
        "ap_recv": 0,
        "sum_sent": 0,
        "sum_recv": 0
    }

    with open('checkpoint.json', 'w') as file:
        json.dump(checkpoint, file, indent=2)

ant_sent = checkpoint["ap_sent"]
ant_recv = checkpoint["ap_recv"]

for file in jsons:
    if(file.__contains__("ap") and file > checkpoint["ap_last_file"]):
        with open(f"bronze-data/{file}") as j:
            content = json.load(j)

            if(ant_sent == 0 and ant_recv == 0):
                ant_sent = content["bytes_sent"]
                ant_recv = content["bytes_recv"]

            checkpoint["ap_last_file"] = file
            checkpoint["ap_sent"] = content["bytes_sent"]
            checkpoint["ap_recv"] = content["bytes_recv"]
            checkpoint["sum_sent"] += content["bytes_sent"]
            checkpoint["sum_recv"] += content["bytes_recv"]

            data["ap_id"].append(content["id_antena"])
            data["ap_bytes_sent"].append(content["bytes_sent"])
            data["ap_bytes_recv"].append(content["bytes_recv"])
            data["active_conn"].append(content["active_conn"])
            data["ap_cpu_usage"].append(content["cpu_usage"])
            data["ap_ram_usage"].append(content["ram_usage"])

            status_message = ""

            if data["active_conn"][-1] > 40:
                status_message += "Alta Densidade "

            if data["ap_cpu_usage"][-1] > 80:
                status_message += "Gargalo de processamento "

            if data["ap_ram_usage"][-1] > 75:
                status_message += "OOM (Out Of Memory)"

            if status_message == "":
                status_message = "Normal"

            data["status"].append(status_message.strip())

    if(file.__contains__("firewall")):
        with open(f"bronze-data/{file}") as j:
            content = json.load(j)

            checkpoint["firewall_last_file"] = file

            data["active_sessions"].append(content["active_sessions"])
            data["dropped_packets"].append(content["dropped_packets"])
            data["top_blocked_ip"].append(content["top_blocked_ip"])
            data["firewall_cpu_usage"].append(content["cpu_usage"])
            data["firewall_ram_usage"].append(content["ram_usage"])

data["firewall_bytes_sent"].append(checkpoint["sum_sent"])
data["firewall_bytes_recv"].append(checkpoint["sum_recv"])

dif_ant_sent = checkpoint["ap_sent"] - ant_sent
dif_ant_recv = checkpoint["ap_recv"] - ant_recv

date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
data["data_registro"].append(date)


mbps_sent = dif_ant_sent * 8 / 60 / 1000000
mbps_recv = dif_ant_recv * 8 / 60 / 1000000

data["mbps_sent"].append(mbps_sent)
data["mbps_recv"].append(mbps_recv)

csv_novo = not os.path.exists("analise.csv")
with open('analise.csv', 'a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    if csv_novo:
        csv_writer.writerow(list(data.keys()))

    linha = []
    for coluna in data.values():
        if len(coluna) > 0:
            linha.append(coluna[-1])
        else:
            linha.append("")   # coluna sem dado nesta execução
    csv_writer.writerow(linha)

with open("checkpoint.json", 'w') as newJson:
    json.dump(checkpoint, newJson, indent=2)
