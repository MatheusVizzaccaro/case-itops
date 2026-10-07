import csv

with open('analise.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    row_sent = []
    row_cpu = []
    ratios = []

    for row in reader:
        row_sent.append({"date": row[0], "mbps_sent": float(row[-2])})
        row_cpu.append({"date": row[0], "cpu_percent": float(row[5])})

    i = 0

while i<row_sent.__len__():
    if(row_cpu[i]["date"] == row_sent[i]["date"]):
        ratios.append(row_cpu[i]["cpu_percent"]/row_sent[i]["mbps_sent"])
    i += 1

print(sorted(ratios))