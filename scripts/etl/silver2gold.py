import csv
import boto3
import os

bucket_name = "s3-itops-bucket-datalake"

s3 = boto3.client("s3", region_name="us-east-1")

response  = s3.get_object(Bucket=bucket_name, Key="silver/analise.csv")
csvfile = response["Body"].read().decode("utf-8").splitlines()

reader = csv.reader(csvfile, delimiter=',')
next(reader)


with open('relatorio.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["date", "relacao_cpu_mbps_sent", "status"])

    for row in reader:
        if len(row) == 0:
            continue

        cpu = row[5]
        mbps = row[-3]
        status = row [-1]

        if cpu == "" or mbps == "" or float(mbps) == 0:
            ratio = ""
        else:
            ratio = float(cpu) / float(mbps)

        csv_writer.writerow([row[0], ratio, status])

s3.upload_file("relatorio.csv", bucket_name, "gold/relatorio.csv")