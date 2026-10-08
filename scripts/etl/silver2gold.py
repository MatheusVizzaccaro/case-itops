import csv
import boto3

bucket_name = "s3-itops-bucket-datalake"

s3 = boto3.client("s3", region_name="us-east-1")

response  = s3.get_object(Bucket=bucket_name, Key="silver/analise.csv")
csvfile = response["Body"].read().decode("utf-8").splitlines()

reader = csv.reader(csvfile, delimiter=',')
next(reader)

with open('relatorio.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["date", "id_access_point", "relacao_cpu_mbps_sent", "relacao_cpu_mbps_recv", "relacao_ram_mbps_sent", "relacao_ram_mbps_recv", "status"])

    for row in reader:
        if len(row) == 0:
            continue

        ap_id = row[1]
        cpu = row[5]
        ram = row[6]
        mbps_sent = row[-3]
        mbps_recv = row[-2]
        status = row [-1]

        if cpu == "" or mbps_sent == "" or float(mbps_sent) == 0:
            ratio_cpu_sent = ""
        else:
            ratio_cpu_sent = float(cpu) / float(mbps_sent)

        if cpu == "" or mbps_recv == "" or float(mbps_recv) == 0:
            ratio_cpu_recv = ""
        else:
            ratio_cpu_recv = float(cpu) / float(mbps_recv)

        if ram == "" or mbps_sent == "" or float(mbps_sent) == 0:
            ratio_ram_sent = ""
        else:
            ratio_ram_sent = float(ram) / float(mbps_sent)

        if ram == "" or mbps_recv == "" or float(mbps_recv) == 0:
            ratio_ram_recv = ""
        else:
            ratio_ram_recv = float(ram) / float(mbps_recv)

        csv_writer.writerow([row[0], ap_id, ratio_cpu_sent, ratio_cpu_recv, ratio_ram_sent, ratio_ram_recv, status])

s3.upload_file("relatorio.csv", bucket_name, "gold/relatorio.csv")