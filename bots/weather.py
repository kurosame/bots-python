""" Get weather from OpenWeatherMap API, then notify LINE Bot """
import os
import json
from urllib.request import urlopen
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from pytz import timezone
from linebot import LineBotApi
from linebot.models import TextSendMessage


def _get_icon(icon_str):
    icon = ""
    if icon_str in ("01d", "01n"):
        icon = "☀️"
    elif icon_str in ("02d", "02n", "03d", "03n", "04d", "04n"):
        icon = "☁️"
    elif icon_str in ("09d", "09n", "10d", "10n"):
        icon = "☂️"
    elif icon_str in ("11d", "11n"):
        icon = "⚡️"
    elif icon_str in ("13d", "13n"):
        icon = "☃️"
    return icon


def _send_to_line(dfg):
    texts = []
    for k, dfv in dfg:
        texts.append(f"【{k}】")
        for _, row in dfv.iterrows():
            texts.append(
                f"{row['time']}時 {_get_icon(row['icon'])} {row['temp']}(℃) {row['rain']}(mm/3h)"
            )
        texts.append("")

    line_bot = LineBotApi(os.getenv("LINE_ACCESS_TOKEN"))
    line_bot.multicast(
        os.getenv("LINE_USER_ID").split(","), TextSendMessage(text="\n".join(texts))
    )


def main():
    """ Get weather from OpenWeatherMap API, then notify LINE Bot """
    url = "http://api.openweathermap.org/data/2.5/forecast"
    place_id = os.getenv("OWM_PLACE_ID")
    api_key = os.getenv("OWM_API_KEY")

    res = urlopen(f"{url}?id={place_id}&appid={api_key}&lang=ja&units=metric").read()
    res_json = json.loads(res)

    arr_rj = []
    for obj in res_json["list"]:
        conv_rj = {}
        timestamp = timezone("Asia/Tokyo").localize(datetime.fromtimestamp(obj["dt"]))
        conv_rj["date"] = timestamp.strftime("%m/%d %a")
        conv_rj["time"] = timestamp.strftime("%H")
        conv_rj["description"] = obj["weather"][0]["description"]
        conv_rj["icon"] = obj["weather"][0]["icon"]
        conv_rj["temp"] = round(obj["main"]["temp"])
        conv_rj["temp_max"] = round(
            obj["main"]["temp_max"]
        )  # Only `16 Day forecast` works
        conv_rj["rain"] = round(obj["rain"]["3h"], 1) if "rain" in obj else 0
        arr_rj.append(conv_rj)

    dframe = pd.DataFrame(arr_rj)
    print(dframe)
    _send_to_line(dframe.groupby("date"))


load_dotenv()
main()
