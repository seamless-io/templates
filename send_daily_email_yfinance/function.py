import os

from dotenv import load_dotenv
import pandas as pd
import yfinance as yf

from send_email import send_email

# Let's load environment variables from .env file
load_dotenv()


def collect_data():
    """
    Collects world indices data.
    :return: list of dicts
    """

    # You can find Major World Indices here: https://finance.yahoo.com/world-indices
    world_indices = ['^GSPC', '^DJI', '^IXIC', '^NYA', '^XAX', '^BUK100P', '^RUT', '^VIX', '^FTSE', '^GDAXI', '^FCHI',
                     '^STOXX50E', '^N100', '^BFX', 'IMOEX.ME', '^N225', '^HSI', '000001.SS', '399001.SZ', '^STI',
                     '^AXJO', '^AORD', '^BSESN', '^JKSE', '^KLSE', '^NZ50', '^KS11', '^TWII', '^GSPTSE', '^BVSP',
                     '^MXX', '^IPSA', '^MERV', '^TA125.TA', '^CASE30', '^JN0U.JO']

    tickers_list = []
    for index in world_indices:
        ticker = yf.Ticker(index)
        tickers_list.append(ticker.info)

    return tickers_list


def transform_data(data):
    """
    Transforms collected data into HTML string.
    :param data: list of dicts
    :return: string
    """
    columns = ['shortName', 'currency', 'regularMarketOpen', 'regularMarketDayHigh', 'regularMarketDayLow',
               'regularMarketPreviousClose']

    df = pd.DataFrame(data)
    table = df.loc[:, columns].to_html()

    return f'<h1>World Indices</h1>{table}'  # Let's add a header to our table


def main():
    """
    By default Seamless Cloud will execute the function `main` in the file `function.py`.
    You can override this behaviour by using --entrypoint flag.
    """
    print('Start executing...')

    sender = os.getenv('SENDER')
    recipient = os.getenv('RECIPIENT')
    password = os.getenv('PASSWORD')
    subject = 'World Indices Daily Report'

    tickers_list = collect_data()
    print('Data collected.')

    body = transform_data(tickers_list)
    print('Data transformed.')

    send_email(sender, recipient, subject, body, password)
    print('Email sent successfully!')
