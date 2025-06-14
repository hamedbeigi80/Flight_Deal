# Flight Deals Finder 🛫

A Python application that automatically searches for cheap flight deals and sends email notifications when prices drop below your specified thresholds.

## Features

- **Automated Flight Search**: Uses the Amadeus API to search for flight deals
- **Price Monitoring**: Compares current prices with your target prices
- **Email Notifications**: Sends alerts when deals are found
- **Direct & Indirect Flights**: Searches both direct and connecting flights
- **Google Sheets Integration**: Manages destinations and user data via Sheety API
- **Multiple Destinations**: Monitor prices for multiple cities simultaneously

## Prerequisites

Before running this application, you'll need:

1. **Amadeus API Account**: Sign up at [Amadeus for Developers](https://developers.amadeus.com/)
2. **Google Sheets**: Create a spreadsheet with your destinations and prices
3. **Sheety Account**: Sign up at [Sheety.co](https://sheety.co/) to connect your Google Sheet
4. **Gmail Account**: For sending email notifications (with app password)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/flight-deals-finder.git
cd flight-deals-finder
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

4. Fill in your API credentials in the `.env` file (see Configuration section)

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Sheety API Configuration
SHEETY_PRICES_ENDPOINT=your_sheety_prices_endpoint
SHEETY_USERS_ENDPOINT=your_sheety_users_endpoint
SHEETY_USERNAME=your_sheety_username
SHEETY_PASSWORD=your_sheety_password

# Amadeus API Configuration
AMADEUS_API_KEY=your_amadeus_api_key
AMADEUS_API_SECRET=your_amadeus_api_secret

# Email Configuration
EMAIL=your_gmail_address
PASSWORD=your_gmail_app_password
SMTP_ADDRESS=smtp.gmail.com
```

### Google Sheets Setup

Create a Google Sheet with two tabs:

#### 1. "prices" tab:
| city | iataCode | lowestPrice |
|------|----------|-------------|
| Paris | | 200 |
| Tokyo | | 500 |
| New York | | 300 |

#### 2. "users" tab:
| firstName | lastName | whatIsYourEmail? |
|-----------|----------|------------------|
| John | Doe | john@example.com |
| Jane | Smith | jane@example.com |

## Usage

1. **Setup your destinations**: Add cities and target prices to your Google Sheet
2. **Add subscribers**: Add email addresses to the users tab
3. **Run the application**:
```bash
python main.py
```

The application will:
- Fetch destination data from your Google Sheet
- Get IATA codes for cities (if not already present)
- Search for flights from London (LON) to each destination
- Compare prices with your target thresholds
- Send email notifications for deals found

## Project Structure

```
flight-deals-finder/
├── main.py                 # Main application entry point
├── data_manager.py         # Handles Google Sheets API interactions
├── flight_search.py        # Amadeus API flight search functionality
├── flight_data.py          # Flight data model and processing
├── notification_manager.py # Email notification system
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore file
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## How It Works

1. **Data Retrieval**: Fetches destination data from Google Sheets via Sheety API
2. **IATA Code Resolution**: Converts city names to airport codes using Amadeus API
3. **Flight Search**: Searches for flights using Amadeus Flight Offers API
4. **Price Comparison**: Compares found prices with target prices
5. **Notification**: Sends email alerts when deals are found

## API Rate Limits

- **Amadeus**: The free tier has limited requests per month
- **Sheety**: Has rate limits on API calls
- The application includes delays between requests to respect these limits

## Email Setup

For Gmail:
1. Enable 2-factor authentication
2. Generate an app password
3. Use the app password (not your regular password) in the `.env` file

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request



## Disclaimer

This application is for educational purposes. Always check airline websites for final booking and verify all flight details before making travel plans.

## Troubleshooting

### Common Issues:

1. **"No flight data" errors**: Usually due to API rate limits or invalid IATA codes
2. **Email sending fails**: Check your Gmail app password and SMTP settings
3. **Sheety API errors**: Verify your endpoint URLs and authentication

### Getting Help:

- Check the API documentation for Amadeus and Sheety
- Ensure all environment variables are correctly set
- Verify your Google Sheets structure matches the expected format

## Acknowledgments

- [Amadeus for Developers](https://developers.amadeus.com/) for flight data API
- [Sheety.co](https://sheety.co/) for Google Sheets API integration
- Built as part of the 100 Days of Code Python course
