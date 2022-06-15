#! /usr/bin/env python

import pandas as pd
import glob
import os
import requests
# setting the path for joining multiple files
files = os.path.join("./resturants", "resturants*.csv")

# list of merged files returned
files = glob.glob(files)

CHUNK_SIZE = 50000
response = requests.get("https://vendors.talabat.com/vendor-list/v1/vendors?areaid=9586&countrycode=1&lat=30.889232680295766&lon=29.571777172386643&fpPaddingStrategy=none").json()
keys = response["vendors"][0].keys()

for csv_file_name in files:
    chunk_container = pd.read_csv(csv_file_name, chunksize=CHUNK_SIZE,low_memory=False,header=None)
    for chunk in chunk_container:
        chunk.to_csv("restaurants.csv", mode="a", index=False)


