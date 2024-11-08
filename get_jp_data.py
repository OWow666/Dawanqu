import random
import time

import requests
import os

base_url = "https://www.toukei.metro.tokyo.lg.jp"

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

full_string = ""
for xx in range(20,23):
    full_string = f"/tnenkan/20{xx:02d}/tn{xx:02d}qv110100.csv"
    url = base_url + full_string
    print(url)
    response = requests.head(url)
    if response.status_code == 200:
        folder_path = f"jp_data/industry"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_response = requests.get(url)
        if file_response.status_code == 200:
            file_path = os.path.join(folder_path, f"20{xx:02d}.csv")
            with open(file_path, "wb") as f:
                f.write(file_response.content)
            print(f"Downloaded! {file_path}")
        else:
            print(f"Download Failed! {file_response.status_code}")
    sleep_time = random.randint(5, 10)
    time.sleep(sleep_time)

