import requests
from twilio.rest import Client

MOBILE_NUMBER = input("Enter your mobile number: ")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API = "1060ALQNDM2A88R9"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "7ca0b3c8a014431e850d918239cd7f98"

TWILIO_SID = "AC7ec8976cfb329dc52fda10fe00d94946"
TWILIO_AUTH_TOKEN="c9123630bc43081b394980f9e3689c89"


# STEP 1: Use https://www.alphavantage.co/documentation/#daily

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
#data_list = [new_item for item in list]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
#print(data_list)
print(yesterday_closing_price)

#day before yesterday closing price
day_bef_yest = data_list[1]
day_bef_closing_price = float(day_bef_yest["4. close"])
print(day_bef_closing_price)

difference = yesterday_closing_price - day_bef_closing_price

if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


diff_perc = round((difference / yesterday_closing_price)*100)
print(diff_perc)


if abs(diff_perc)>5:
    news_params={
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)


    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_perc}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message=client.messages.create(
            body=article,
            from = "+12073379770",
            to=MOBILE_NUMBER
        )


