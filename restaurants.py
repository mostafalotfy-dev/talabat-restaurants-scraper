#!/usr/bin/env python
from time import sleep
import requests
import pandas as pd
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("language",help="enter the language (ar-KW,en-US)",choices=("en-US","ar-KW"))
parser.add_argument("suffix",help="the csv output file suffix")
parser.add_argument("areanumber")
args = parser.parse_args()

headers = {
    "x-should-use-vendors-microservice": "false",
    "traceparent": "00-da7d6fe73fe04b5a82cfdf615d335bf1--00",
    "newrelic": "eyJ2IjpbMCwyXSwiZCI6eyJkLnR5IjoiTW9iaWxlIiwiZC5hYyI6IjkzODk1OCIsImQuYXAiOiI0MTQ0NjE2MzgiLCJkLnRyIjoiZGE3ZDZmZTczZmUwNGI1YTgyY2ZkZjYxNWQzMzViZjEiLCJkLmlkIjoiOGRjYzM4NDc3MjVhNDA3MyIsImQudGkiOjE2NTQ1NTQyMjc4MDR9fQ==",
    "tracestate": "@nr=0-2-938958-414461638-----1654554227804",
    "accept-language":args.language,
    "x-device-source": "6",
    "brandtype": "1",
    "appbrand": "1",
    "x-perseussessionid": "1654554088453.4195723680.xmqihozdly",
    "x-perseusclientid": "1654524051085.1792648035.layxejczwk",
    "x-device-version": "8.92",
    "x-device-id": "71a3774f2f89e7b",
    "x-talabat-android-installation-path": "L2RhdGEvdXNlci8wL2NvbS50YWxhYmF0",
    "x-talabat-android-package-name": "com.talabat",
    "accept-encoding":"gzip",
    "user-agent":"okhttp/4.9.2",
    "x-newrelic-id": "XQUPWFNbGwcBUFVUBgcEXg=="
  }
cookies = {"__cf_bm":".25KquhS2iYyCQtF82QAdk2sQ-1654550601-0-AdaN290vKqUcOOkxHWg2DlgVUK1NakV8379WnLvcqyxVtp00Pe6cHnu74/LW8hK2btWV75v6DsQ5kIPlRTvpSKtrS63lgzlVKUQ9EG3/uDRn",
    "AWSALB":"75EuMmE23AsGI5uSt0MnjgWPv31SERrfaxYTq3YkBGQj/H0M7V9f4VxmqEkQgmY9dqTv/jsILYpkNj92iL5RauZIi4LQxwkp2BxSh8yYNuD+hosiE19TmVxnvLt1ZnDzBuVNInATHV9VS4",
    "AWSALBCORS":"75EuMmE23AsGI5uStTq3YkBGQj/H0M7V9f4VxmqEkQgmY9dqTv/jsILYpkNj92iL5RauZIi4LQxwkp2BxSh8yYNuD+hosiE19TmVxnvLt1ZnDzBuVNInATHV9VS4"}

def scrape(result,n):
    while True:
        n+=1
       
        result = results[n]
        if result["polc"] != "":
            lat,long = result["polc"].split(",")
            link = ("https://vendors.talabat.com/vendor-list/v1/vendors?areaid={}&countrycode={}&lat={}&lon={}&page=1&size=100000&vertical_id=0&fpPaddingStrategy=none"
            .format(result["id"],args.areanumber,lat,long))
            response = requests.get(link,headers=headers,cookies=cookies)
            if len(response.text) > 0:
                jsonResponse = response.json()
                jsonResponse["areanumber"] = args.areanumber
                df = pd.DataFrame(jsonResponse["vendors"])
                if "cus" in df:
                    categories = df.pop("cus")        
                    for category in categories:
                        pd.DataFrame(category).to_csv(open("categories%s.csv"%args.suffix,"a"),header=False)
                    df.to_csv(open("resturants_{}.csv".format(args.suffix),"a"),header=False)
            open("{}_id".format(args.suffix),"w").write(str(n))
            sleep(10) # bybass cloudflare , do not change it
        

jsonresponse = requests.get('https://api.talabat.com/apiAndroid/v1/apps/areas/{}'.format(args.areanumber))

jsonresponse = jsonresponse.json()

results = jsonresponse["result"]

if __name__ == "__main__":
    if os.path.exists("{}_id".format(args.suffix)):
            f = open("{}_id".format(args.suffix),"r")
            n = int(f.read())
            n += 1
            f.close()
            scrape(results[n],n)
    else:
       scrape(results[0],0)
        

