import os

import yfinance as yf

if __name__ == '__main__':
    ticker = yf.Ticker(os.getenv('COMPANY_TICKER'))
    print(f"Company: {ticker.info['longName']}")
    print(f"Stock Price: ${ticker.info['regularMarketPrice']}")
    print("Latest 3 recommendations:")
    for date, row in ticker.recommendations.iloc[-3:].iterrows():
        print(f"{row['Firm']} recommendation dated {date.date()}: {row['To Grade']}")
    print("\n" + "#"*20)
    print("This script is purely for demonstration purposes. "
          "Do you want to try something more useful that sends you a daily email? "
          "We have a template for this - it's called 'Send daily Email with World Indices pices'. "
          "You can find it on the Templates tab. Have fun exploring our templates!")
    print("#" * 20)
