import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
VERIFIED_NUMBER = "your own phone number verified with Twilio"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "YOUR OWN API KEY FROM ALPHAVANTAGE"
NEWS_API_KEY = "YOUR OWN API KEY FROM NEWSAPI"
TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

# ------------------------- Send request to stock API ----------------------------- #

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}  # Required params for request

response = requests.get(STOCK_ENDPOINT, params=stock_params)  # send request for data
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]

# Get yesterday's closing stock price
yesterday_closing_price = yesterday_data["4. close"]  # yesterday's closing stock price (its string)
print(yesterday_closing_price)

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

# ------------------------------- Functionality ---------------------------------- #
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)


# When stock price increase/decreases by 5% between yesterday and the day before yesterday then Get News.
if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)  # get news from https://newsapi.org/
    articles = news_response.json()["articles"]

    three_articles = articles[:3]
    print(three_articles)

    # Create a new list of the first 3 articles headline and description
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}." \
                          f" \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)
    # ---------------------------------------- Send sms ------------------------------- #
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # Send each article as a separate message via Twilio.
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
