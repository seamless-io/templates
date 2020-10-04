import os
from datetime import datetime

import gspread
import yfinance as yf
from oauth2client.service_account import ServiceAccountCredentials

# You can find Major World Indices here: https://finance.yahoo.com/world-indices
INDICES = os.getenv('INDICES', '^GSPC')  # If not provided, let's collect S&P 500 by default

JSON_KEYFILE = os.getenv('JSON_KEYFILE')  # The file you get after generating Google Spreadsheet API key
SHEET_ID = os.getenv('SHEET_ID')  # You can get Sheet ID from URL
SHEET_NAME = os.getenv('SHEET_NAME')  # The name of the sheet where to insert data
SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']


def get_gs_client(json_keyfile, scope):
    """
    Construct a Gspread object from JSON keyfile by name.
    :param str json_keyfile: the list of tickers
    :param list scope: the list of scopes
    :return `client_class` instance:
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)
    return client


def collect_indices(indices):
    """
    Collects indices data.
    :param list indices: the list of tickers
    :return list: The list of lists
    """
    tickers_list = []
    for index in indices:
        ticker = yf.Ticker(index)
        name = ticker.info['shortName']
        price_close = ticker.info['ask']  # The ask price refers to the lowest price a seller will accept for a security
        date = str(datetime.now())
        tickers_list.append([name, price_close, date])

    return tickers_list


def append_records(gsheet_id, sheet_name, records):
    """
    Collects indices data.
    :param gsheet_id str:
    :param sheet_name str:
    :param records list:
    :return None:
    """
    gclient = get_gs_client(JSON_KEYFILE, SCOPE)
    advisers_sheet = gclient.open_by_key(gsheet_id)
    advisers_sheet.worksheet(sheet_name).append_rows(records, 'USER_ENTERED')


def main():
    indices = INDICES.split(',')
    fetched_indices = collect_indices(indices)
    append_records(SHEET_ID, SHEET_NAME, fetched_indices)


if __name__ == '__main__':
    main()
