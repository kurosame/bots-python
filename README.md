# Bots with Python

## [Weather](https://github.com/kurosame/bots-python/blob/master/bots/weather.py)

Get weather from OpenWeatherMap API, then notify LINE Bot

To run it, create `.env` file then set the following

```sh
OWM_PLACE_ID      # OpenWeatherMap API place name id
OWM_API_KEY       # OpenWeatherMap API api key
LINE_ACCESS_TOKEN # LINE Messaging API access token
LINE_USER_ID      # LINE User ID (When multiple users, Separate to comma)
```

## [Nippan GPT](https://github.com/kurosame/nippan-gpt)

Have daily sales reports responded to in Slack using Azure GPT

## pre-commit

If you use [pre-commit](https://github.com/pre-commit/pre-commit), run the following

```sh
brew install pre-commit
pre-commit install
```
