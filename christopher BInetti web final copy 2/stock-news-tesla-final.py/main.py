import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "60QZFG3AQLYTTS3N"
NEWS_API_KEY = "33dafa93b89441528bc8b2da07002362"
TWILIO_SID = "AC6403bfc5a31edd3d01c275fd90467c85"
TWILIO_AUTH_TOKEN = "b2738bd18c05fd8ec46790c0a4aab005"
    # Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "TIME_SERIES_DAILY",  #THIS IS A FUNCTION FOUND AT DOCUMENTION DAILY
    "symbol": STOCK_NAME,       #these two are to select the which stock we are trying to find.
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]     #using json because its in a more readable format
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]  # all info for yesterdays stock
yesterday_closing_price = yesterday_data['4. close']   # retreiving end of day price 'ending price'
print(yesterday_closing_price)

#Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]  # all info for yesterdays stock
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']   # retreiving end of day price 'ending price'
print(day_before_yesterday_closing_price)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))  # abs just returns the absolute value ex. if - returns a +
print(difference)
# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = difference / float(yesterday_closing_price) * 100

print(diff_percent)            #   !!!!!!! take the top code out of # just doing this temp so i can see if it works!!!!!!!!
#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
#change it later to be greater then 5
if diff_percent > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    print(articles)


# Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]

## STEP 3: Use twilio.com/docs/sms/quickstart/python
#to send a separate message with each article's title and description to your phone number.

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+18556101149",
            to="8177075834"
        )

#TODO 9. - Send each article as a separate message via Twilio.
# we now need to import twilio
#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

