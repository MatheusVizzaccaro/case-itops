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
        'ram_usage': psutil.virtual_memory().percent
    }

    date = datetime.datetime.now().strftime('%y-%m-%d-%H-%M')

    s3.put_object(
        Bucket=bucket_name,
        Key=f"bronze/firewall01_{date}.json",
        Body=json.dumps(data, indent=2)
    )

    time.sleep(60)