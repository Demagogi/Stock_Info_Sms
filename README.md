# Stock_Info_Sms
Sends sms to the phone.
This program sends request to https://www.alphavantage.co/ API, and retrieves information about Tesla stocks price.<br>
also sends request to https://newsapi.org/ API to retrive News about Tesla stocks.<br>
compares yesterday's closing stock price to before yesterday's closing stock price and shows difference in percents.<br>
if that difference is more then 5%, sends Sms with text from newsapi to our phone with https://www.twilio.com/ API.
