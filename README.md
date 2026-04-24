# ✈️ Flight Deal Finder
 
A Python automation tool that monitors flight prices and sends you an alert when a cheap deal is found.
 
## How It Works
 
The program reads destination cities and their lowest acceptable prices from a Google Sheet. It then searches for flights using SerpAPI and sends you a WhatsApp or SMS notification via Twilio if a cheaper price is found.
 
## Project Structure
 
```
flight-deals/
├── main.py                 # Entry point — ties everything together
├── data_manager.py         # Reads and writes data to Google Sheet via Sheety
├── flight_search.py        # Searches for flights using SerpAPI
├── flight_data.py          # Structures the flight data into an object
├── notification_manager.py # Sends SMS/WhatsApp alerts via Twilio
├── .env                    # Secret keys (never commit this to GitHub)
└── requirements.txt        # Python dependencies
```
 
## APIs Used
 
| Service | Purpose | Free Tier |
|---|---|---|
| [Sheety](https://sheety.co) | Read/write Google Sheet data | 200 requests/month |
| [SerpAPI](https://serpapi.com) | Search Google Flights | 100 searches/month |
| [Twilio](https://twilio.com) | Send SMS or WhatsApp alerts | Trial credits |
 
## Setup
 
### 1. Clone the project and install dependencies
 
```bash
pip install requests python-dotenv twilio
```
 
### 2. Set up your Google Sheet
 
Create a Google Sheet with the following columns:
 
| city | iataCode | lowestPrice |
|------|----------|-------------|
| Paris | CDG | 500 |
| New York | JFK | 800 |
| Tokyo | NRT | 956 |
 
### 3. Connect Sheety to your Google Sheet
 
- Go to [sheety.co](https://sheety.co) and sign in with the same Google account that owns the sheet
- Create a new project and paste your Google Sheet URL
- Enable **GET** and **PUT** under APIs
- Enable **Bearer Token** authentication and set your own token
### 4. Register with SerpAPI
 
- Sign up at [serpapi.com](https://serpapi.com)
- Copy your API key from the dashboard
### 5. Register with Twilio
 
- Sign up at [twilio.com](https://twilio.com)
- Get your Account SID, Auth Token, and a Twilio phone number
### 6. Create your `.env` file
 
Create a `.env` file in the root of the project and fill in your credentials:
 
```
SHEETY_URL=https://api.sheety.co/your_username/your_project/prices
SHEETY_TOKEN=your_bearer_token
 
SERPAPI_API_KEY=your_serpapi_key
 
TWILIO_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_FROM=whatsapp:+14155238886
TWILIO_TO=whatsapp:+your_number
```
 
> ⚠️ Never share your `.env` file or upload it to GitHub.
 
## Running the Program
 
```bash
python main.py
```
 
The program will:
1. Read all destination cities from your Google Sheet
2. Search for the cheapest flights for each city (from tomorrow up to 6 months ahead)
3. Send you a WhatsApp/SMS message if a price lower than your threshold is found
## Example Notification
 
```
Low price alert! Only £320 to fly from TBS to CDG on 2024-06-15 until 2024-06-22!
```
 
## Notes
 
- Keep your Google Sheet to 3–5 cities to avoid burning through free API limits during development
- Use `requests_cache` to cache SerpAPI responses locally while testing so you don't waste searches
- Twilio SMS may not work in all countries — use WhatsApp as a fallback