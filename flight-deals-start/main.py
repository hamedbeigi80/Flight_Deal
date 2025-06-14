#!/usr/bin/env python3
"""
Flight Deals Finder

This application searches for cheap flight deals and sends email notifications
when prices drop below specified thresholds.

Author: Hamed Ahmadbeigi
Date: 2024
"""

import time
from datetime import timedelta, datetime
from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# Configuration
ORIGIN_CITY_IATA = "LON"  # London as the departure city

def main():
    """Main function to run the flight deals finder."""
    print("🛫 Starting Flight Deals Finder...")
    
    # Initialize managers
    data_manager = DataManager()
    flight_search = FlightSearch()
    
    # Get destination data from Google Sheet
    print("📊 Fetching destination data...")
    sheet_data = data_manager.get_destination_data()
    
    # Get IATA codes for cities that don't have them
    print("🏙️ Getting IATA codes for cities...")
    for row in sheet_data:
        if row["iataCode"] == "":
            print(f"Getting IATA code for {row['city']}...")
            row["iataCode"] = flight_search.get_destination_code(row["city"])
            # Slow down requests to avoid rate limit
            time.sleep(2)
    
    # Update the Google Sheet with IATA codes
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()
    
    # Get customer email list
    print("📧 Getting customer email list...")
    customer_data = data_manager.get_customer_emails()
    customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]
    print(f"Found {len(customer_email_list)} subscribers")
    
    # Set search dates (tomorrow to 6 months from now)
    tomorrow = datetime.now() + timedelta(days=1)
    six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
    
    print(f"🔍 Searching for flights from {tomorrow.strftime('%Y-%m-%d')} to {six_month_from_today.strftime('%Y-%m-%d')}")
    
    # Search for flights to each destination
    for destination in sheet_data:
        print(f"\n🎯 Getting flights for {destination['city']}...")
        
        # Search for direct flights first
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today
        )
        cheapest_flight = find_cheapest_flight(flights)
        print(f"{destination['city']}: £{cheapest_flight.price}")
        
        # Wait to avoid rate limits
        time.sleep(2)
        
        # If no direct flights found, search for indirect flights
        if cheapest_flight.price == "N/A":
            print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
            stopover_flights = flight_search.check_flights(
                ORIGIN_CITY_IATA,
                destination["iataCode"],
                from_time=tomorrow,
                to_time=six_month_from_today,
                is_direct=False
            )
            cheapest_flight = find_cheapest_flight(stopover_flights)
            print(f"Cheapest indirect flight price is: £{cheapest_flight.price}")
        
        # Check if we found a deal (price below threshold)
        if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
            print(f"🎉 DEAL FOUND! Price £{cheapest_flight.price} is below threshold £{destination['lowestPrice']}")
            
            # Create notification message
            notification_manager = NotificationManager()
            if cheapest_flight.stops == 0:
                message = (f"Low price alert! Only GBP {cheapest_flight.price} to fly direct "
                          f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                          f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}.")
            else:
                message = (f"Low price alert! Only GBP {cheapest_flight.price} to fly "
                          f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                          f"with {cheapest_flight.stops} stop(s) "
                          f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}.")
            
            print(f"📤 Sending notifications to {len(customer_email_list)} subscribers...")
            
            # Send emails to everyone on the list
            notification_manager.send_emails(email_list=customer_email_list, email_body=message)
            print("✅ Notifications sent!")
        else:
            print("💰 No deals found for this destination.")
    
    print("\n🏁 Flight search completed!")


if __name__ == "__main__":
    main()
