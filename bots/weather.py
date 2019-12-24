import json
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from pytz import timezone
from urllib.request import urlopen


def main():
    url = "http://api.openweathermap.org/data/2.5/forecast"
    id = os.getenv("PLACE_ID")
    api_key = os.getenv("API_KEY")

    res = urlopen(f"{url}?id={id}&appid={api_key}&lang=ja&units=metric").read()
    res_json = json.loads(res)

    arr_rj = []
    for rj in res_json["list"]:
        conv_rj = {}
        timestamp = timezone("Asia/Tokyo").localize(datetime.fromtimestamp(rj["dt"]))
        conv_rj["date"] = timestamp.strftime("%m/%d %a")
        conv_rj["time"] = timestamp.strftime("%H")
        conv_rj["description"] = rj["weather"][0]["description"]
        conv_rj["icon"] = rj["weather"][0]["icon"]
        conv_rj["temp"] = round(rj["main"]["temp"])
        conv_rj["rain"] = round(rj["rain"]["3h"], 1) if "rain" in rj else 0
        arr_rj.append(conv_rj)

    print(pd.DataFrame(arr_rj).groupby("date").groups)
    print(pd.DataFrame(arr_rj).groupby("date").get_group("12/29 Sun"))


load_dotenv()
main()
