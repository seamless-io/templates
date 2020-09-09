"""
By default Seamless Cloud will execute the file `function.py`.
You can override this behaviour by using --entrypoint flag.
"""
import datetime
import urllib

import requests
from bs4 import BeautifulSoup

session = requests.Session()
today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(1)

REQUEST_HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 "
                  "Safari/537.36"}
BOOKING_PREFIX = 'https://www.booking.com'

# https://core.telegram.org/bots
BOT_API_KEY = 'Your bot api key, it looks something like "110301563:AAHdqTcvCH1vGWJxfSeoffAs0K5PsLDsaw"'
CHANNEL_NAME = 'the name of a public channel with a "@" at the beginning, like "@my_channel"'


class Hotel:
    raw_html = None
    name = None
    score = None
    price = None
    link = None
    details = None

    def __init__(self, raw_html):
        self.raw_html = raw_html
        self.name = get_hotel_name(raw_html)
        self.score = get_hotel_score(raw_html)
        self.price = get_hotel_price(raw_html)
        self.link = get_hotel_detail_link(raw_html)

    def get_details(self):
        if self.link:
            self.details = HotelDetails(self.link)


class HotelDetails:
    latitude = None
    longitude = None

    def __init__(self, details_link):
        detail_page_response = session.get(BOOKING_PREFIX + details_link, headers=REQUEST_HEADER)
        soup_detail = BeautifulSoup(detail_page_response.text, "lxml")
        self.latitude = get_coordinates(soup_detail)[0]
        self.longitude = get_coordinates(soup_detail)[1]


def create_url(people, country, city, date_in, date_out, rooms, score_filter):
    url = f"https://www.booking.com/searchresults.en-gb.html?selected_currency=USD&checkin_month={date_in.month}" \
          f"&checkin_monthday={date_in.day}&checkin_year={date_in.year}&checkout_month={date_out.month}" \
          f"&checkout_monthday={date_out.day}&checkout_year={date_out.year}&group_adults={people}" \
          f"&group_children=0&order=price&ss={city}%2C%20{country}" \
          f"&no_rooms={rooms}"
    if score_filter:
        if score_filter == '9+':
            url += '&nflt=review_score%3D90%3B'
        elif score_filter == '8+':
            url += '&nflt=review_score%3D80%3B'
        elif score_filter == '7+':
            url += '&nflt=review_score%3D70%3B'
        elif score_filter == '6+':
            url += '&nflt=review_score%3D60%3B'
    return url


def get_result(people, country, city, date_in, date_out, rooms, score_filter):
    result = []
    data_url = create_url(people, country, city, date_in, date_out, rooms, score_filter)
    response = session.get(data_url, headers=REQUEST_HEADER)
    soup = BeautifulSoup(response.text, "lxml")
    hotels = soup.select("#hotellist_inner div.sr_item.sr_item_new")
    for hotel in hotels:
        result.append(Hotel(hotel))
    session.close()
    return result


def get_hotel_name(hotel):
    identifier = "span.sr-hotel__name"
    if hotel.select_one(identifier) is None:
        return ''
    else:
        return hotel.select_one(identifier).text.strip()


def get_hotel_score(hotel):
    identifier = "div.bui-review-score__badge"
    if hotel.select_one(identifier) is None:
        return ''
    else:
        return hotel.select_one(identifier).text.strip()


def get_hotel_price(hotel):
    identifier = "div.bui-price-display__value.prco-text-nowrap-helper.prco-inline-block-maker-helper"
    if hotel.select_one(identifier) is None:
        return ''
    else:
        return hotel.select_one(identifier).text.strip()[2:]


def get_hotel_detail_link(hotel):
    identifier = ".txp-cta.bui-button.bui-button--primary.sr_cta_button"
    if hotel.select_one(identifier) is None:
        return ''
    else:
        return hotel.select_one(identifier)['href']


def get_coordinates(soup_detail):
    coordinates = []
    if soup_detail.select_one("#hotel_sidebar_static_map") is None:
        coordinates.append('')
        coordinates.append('')
    else:
        coordinates.append(soup_detail.select_one("#hotel_sidebar_static_map")["data-atlas-latlng"].split(",")[0])
        coordinates.append(soup_detail.select_one("#hotel_sidebar_static_map")["data-atlas-latlng"].split(",")[1])
    return coordinates


def send_message(html):
    resp = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage?parse_mode=HTML&'
                        f'chat_id={CHANNEL_NAME}&'
                        f'text={urllib.parse.quote_plus(html)}')
    resp.raise_for_status()


def send_location(latitude, longitude):
    resp = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendlocation?'
                        f'chat_id={CHANNEL_NAME}&'
                        f'latitude={latitude}&longitude={longitude}')
    resp.raise_for_status()


def main():
    search_params = {
        'people': 4,
        'rooms': 2,
        'country': 'Ukraine',
        'city': 'Bukovel',
        'date_in': datetime.datetime(2020, 12, 31).date(),
        'date_out': datetime.datetime(2021, 1, 2).date(),
        'score_filter': '9+'
    }

    print(f"Searching hotels using parameters: {search_params}")
    result = get_result(**search_params)
    top_3 = result[:3]
    send_message(
        f'Here are your search results for {search_params["people"]} people, {search_params["rooms"]} rooms in '
        f'{search_params["city"]}, {search_params["country"]} for dates from {search_params["date_in"]} to '
        f'{search_params["date_out"]} with {search_params.get("score_filter", "any")} rating')
    for hotel in top_3:
        send_message(f'<a href="{BOOKING_PREFIX}{hotel.link}">{hotel.name} </a> ({hotel.score})\n'
                     f'Total price: {hotel.price}')
        hotel.get_details()
        send_location(hotel.details.latitude, hotel.details.longitude)
    print('Notifications were sent successfully')


if __name__ == '__main__':
    main()
