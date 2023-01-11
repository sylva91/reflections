import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

url = 'https://www.skyscanner.com/transport/flights/CDG/anywhere/{}/'

def get_flight_info(departure_date):
    url = url.format(departure_date)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    flight_info = soup.find_all('span', class_='BpkText_bpk-text__2NHsO')
    return flight_info

def filter_flights(flight_info, departure_time_filter, return_time_filter,price_filter):
    filtered_flights = []
    for flight in flight_info:
        departure_time = datetime.strptime(flight.text.strip()[:5], '%H:%M')
        if departure_time.time() > departure_time_filter and '€' in flight.text:
            price = int(flight.text.strip()[-4:].replace(".",""))
            if price < price_filter:
                return_time = datetime.strptime(flight.text.strip()[-5:], '%H:%M')
                if return_time.time() > return_time_filter:
                    filtered_flights.append(flight)
    return filtered_flights

september_2023 = [date(2023,9,day).strftime('%Y-%m-%d') for day in range(1,31)]
for flight_date in september_2023:
    flight_info = get_flight_info(flight_date)
    filtered_flight_info = filter_flights(flight_info, 
                                            datetime.strptime('19:00','%H:%M').time(), 
                                            datetime.strptime('14:00','%H:%M').time(),
                                            100)
    print(f'{flight_date} : {filtered_flight_info}')
