import csv

with open('analise.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    row_sent = []
    row_cpu = []

    for row in reader:
        row_sent.append({"date": row[0], "mbps_sent": float(row[-2])})
        row_cpu.append({"date": row[0], "mbps_sent": float(row[5])})


print(row_cpu)
print(row_sent)
