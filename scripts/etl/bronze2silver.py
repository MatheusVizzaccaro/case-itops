import os
import json
import csv

jsons = os.listdir("bronze-data/")

data = {
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
    "firewall_bytes_recv": []
}




for file in jsons:
    if(file.__contains__("firewall")):
        with open(f"bronze-data/{file}") as j:
            content = json.load(j)

            data["active_sessions"].append(content["active_sessions"])
            data["dropped_packets"].append(content["dropped_packets"])
            data["top_blocked_ip"].append(content["top_blocked_ip"])
            data["firewall_cpu_usage"].append(content["cpu_usage"])
            data["firewall_ram_usage"].append(content["ram_usage"])
            data["firewall_bytes_sent"].append(content["bytes_sent"])
            data["firewall_bytes_recv"].append(content["bytes_recv"])
            
    if(file.__contains__("ap")):
        with open(f"bronze-data/{file}") as j:
            content = json.load(j)

            data["ap_id"].append(content["id_antena"])
            data["ap_bytes_sent"].append(content["bytes_sent"])
            data["ap_bytes_recv"].append(content["bytes_recv"])
            data["active_conn"].append(content["active_conn"])
            data["ap_cpu_usage"].append(content["cpu_usage"])
            data["ap_ram_usage"].append(content["ram_usage"])

with open('analise.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(list(data.keys()))

    for i in range(len(data["ap_id"])):
        linha = []
        for coluna in data.values():
            linha.append(coluna[i])
        csv_writer.writerow(linha)
