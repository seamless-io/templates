import os
import requests
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# You can find more crypto assets here: https://messari.io/
CRYPTO = os.getenv('CRYPTO', 'BTC')  # If not provided, let's collect Bitcoin by default

JSON_KEYFILE = os.getenv('JSON_KEYFILE')  # The file you get after generating Google Spreadsheet API key
SHEET_ID = os.getenv('SHEET_ID')  # You can get Sheet ID from a Google Spreadsheet URL
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


def collect_crypto(crypto):
    """
    Collects crypto data.
    :param str crypto: the crypto asset name
    :return list: The list like ['BTC', 1029.34, '2020-01-01 10:00:00'']
    """
    url = f'https://data.messari.io/api/v1/assets/{crypto}/metrics'
    resp = requests.get(url)
    data = resp.json()
    price = data['data']['market_data']['price_usd']
    date = str(datetime.now())
    return [crypto, price, date]


def append_record(gsheet_id, sheet_name, record):
    """
    Collects indices data.
    :param gsheet_id str:
    :param sheet_name str:
    :param record list:
    :return None:
    """
    gclient = get_gs_client(JSON_KEYFILE, SCOPE)
    advisers_sheet = gclient.open_by_key(gsheet_id)
    # Find more methods here: https://gspread.readthedocs.io/en/latest/api.html
    advisers_sheet.worksheet(sheet_name).append_row(record, 'USER_ENTERED')


def main():
    print('Start executing...')
    crypto_data = collect_crypto(CRYPTO)
    print(f'{CRYPTO} price: {crypto_data[1]}')
    append_record(SHEET_ID, SHEET_NAME, crypto_data)
    print('Finish executing.')


if __name__ == '__main__':
    main()
