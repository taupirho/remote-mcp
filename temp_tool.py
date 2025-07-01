from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="stockChecker", stateless_http=True)

import requests
from datetime import datetime, timedelta

# This helper function can be reused. It's not tied to a specific API provider.
def get_coords_for_city(city_name):
    """
    Converts a city name to latitude and longitude using a free, open geocoding service.
    """
    # Using Open-Meteo's geocoding, which is also free and requires no key.
    GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
    params = {'name': city_name, 'count': 1, 'language': 'en', 'format': 'json'}
    
    try:
        response = requests.get(GEO_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('results'):
            print(f"Error: City '{city_name}' not found.")
            return None, None
            
        # Extract the very first result
        location = data['results'][0]
        return location['latitude'], location['longitude']
        
    except requests.exceptions.RequestException as e:
        print(f"API request error during geocoding: {e}")
        return None, None

@mcp.tool()
def get_historical_weekly_high(city_name):
    """
    Gets the highest temperature for a city over the previous 7 days using the
    commercially-friendly Open-Meteo API.

    Args:
        city_name (str): The name of the city (e.g., "New York", "London").

    Returns:
        float: The highest temperature in Fahrenheit from the period, or None if an error occurs.
    """
    # 1. Get the coordinates for the city
    lat, lon = get_coords_for_city(city_name)
    if lat is None or lon is None:
        return None # Exit if city wasn't found
        
    # 2. Calculate the date range for the last week
    end_date = datetime.now() - timedelta(days=1)
    start_date = datetime.now() - timedelta(days=7)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # 3. Prepare the API request for the Historical API
    HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/era5"
    params = {
        'latitude': lat,
        'longitude': lon,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'daily': 'temperature_2m_max', # The specific variable for daily max temp
        'temperature_unit': 'fahrenheit' # This API handles units correctly
    }
    
    try:
        print(f"Fetching historical weekly max temp for {city_name.title()}...")
        response = requests.get(HISTORICAL_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        daily_data = data.get('daily', {})
        max_temps = daily_data.get('temperature_2m_max', [])
        
        if not max_temps:
            print("Could not find historical temperature data in the response.")
            return None
            
        # 4. Find the single highest temperature from the list of daily highs
        highest_temp = max(max_temps)
        
        return round(highest_temp, 1)

    except requests.exceptions.RequestException as e:
        print(f"API request error during historical fetch: {e}")
        return None