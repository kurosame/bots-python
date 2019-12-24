import json
import os
from dotenv import load_dotenv
from urllib.request import urlopen


def main():
    url = "http://api.openweathermap.org/data/2.5/forecast"
    id = os.getenv("PLACE_ID")
    api_key = os.getenv("API_KEY")

    res = urlopen(f"{url}?id={id}&appid={api_key}").read()
    res_json = json.loads(res)


load_dotenv()
main()
