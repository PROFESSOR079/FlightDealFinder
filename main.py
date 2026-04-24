import time
import requests_cache
from pprint import pprint
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight

requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    }
)

data_manager = DataManager()
flight_search = FlightSearch()

sheet_data = data_manager.get_destination_data()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
return_date_str = six_month_from_today.strftime("%Y-%m-%d")

ORIGIN_CITY_IATA = "LHR"

for destination in sheet_data:
    print(f"--- Checking flights for {destination['city']} ---")

    try:
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today
        )

        cheapest_flight = find_cheapest_flight(flights, return_date=return_date_str)
        print(f"Result: {destination['city']} - GBP {cheapest_flight.price}")

        if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
            print(f"!!! Lower price found for {destination['city']} !!!")
            data_manager.update_lowest_price(destination["id"], cheapest_flight.price)
        else:
            print(f"No cheaper flights for {destination['city']}.")

    except Exception as e:
        print(f"An error occurred for {destination['city']}: {e}")

    print("Waiting 2 seconds before next search...")
    time.sleep(2)

print("\n--- All destinations checked! ---")