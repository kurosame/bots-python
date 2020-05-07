import os
import json
import pandas as pd
from dotenv import load_dotenv
from urllib.request import urlopen
from datetime import datetime
from pytz import timezone
from linebot import LineBotApi
from linebot.models import TextSendMessage


def get_weather_icon(icon_str):
    if icon_str == "01d" or icon_str == "01n":
        return "☀️"
    elif (
        icon_str == "02d"
        or icon_str == "02n"
        or icon_str == "03d"
        or icon_str == "03n"
        or icon_str == "04d"
        or icon_str == "04n"
    ):
        return "☁️"
    elif (
        icon_str == "09d" or icon_str == "09n" or icon_str == "10d" or icon_str == "10n"
    ):
        return "☂️"
    elif icon_str == "11d" or icon_str == "11n":
        return "⚡️"
    elif icon_str == "13d" or icon_str == "13n":
        return "☃️"
    else:
        return ""


def send_to_line(dfg):
    texts = []
    for k, df in dfg:
        texts.append(f"【{k}】")
        for _, d in df.iterrows():
            texts.append(
                f"{d['time']}時 {get_weather_icon(d['icon'])} {d['temp']}(℃) {d['rain']}(mm/3h)"
            )
        texts.append("")

    line_bot = LineBotApi(os.getenv("LINE_ACCESS_TOKEN"))
    line_bot.multicast(
        os.getenv("LINE_USER_ID").split(","), TextSendMessage(text="\n".join(texts))
    )


def main():
    url = "http://api.openweathermap.org/data/2.5/forecast"
    id = os.getenv("OWM_PLACE_ID")
    api_key = os.getenv("OWM_API_KEY")

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
        conv_rj["temp_max"] = round(rj["main"]["temp_max"]) # Only `16 Day forecast` works
        conv_rj["rain"] = round(rj["rain"]["3h"], 1) if "rain" in rj else 0
        arr_rj.append(conv_rj)

    df = pd.DataFrame(arr_rj)
    print(df)
    send_to_line(df.groupby("date"))


load_dotenv()
main()
