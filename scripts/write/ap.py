import psutil
import random
import json
import datetime
import boto3
import time
import os
from dotenv import load_dotenv

load_dotenv()

bucket_name = "s3-itops-bucket-datalake"

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),   
    region_name="us-east-1",
)

s3 = session.client("s3")

while True:
    data = {
        'id_antena': random.randint(0,10),
        'bytes_sent': psutil.net_io_counters().bytes_sent,
        'bytes_recv': psutil.net_io_counters().bytes_recv,
        'active_conn': random.randint(5,50),
        'cpu_usage': psutil.cpu_percent(),
        'ram_usage': psutil.virtual_memory().percent
    }

    date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')


    s3.put_object(
        Bucket=bucket_name,
        Key=f"bronze/ap01_{date}.json",
        Body=json.dumps(data, indent=2)
    )

    time.sleep(60)