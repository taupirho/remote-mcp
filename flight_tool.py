import os

@mcp.tool()
def get_flight_info(flight_number):
    print(f"🔍 Running get_flight_info with: {flight_number}")
    print(f"🔐 API KEY: {os.environ.get('AVIATIONSTACK_API_KEY')[:5]}...")

    AVIATIONSTACK_API_KEY = os.environ.get("AVIATIONSTACK_API_KEY")
    params = {'access_key': AVIATIONSTACK_API_KEY, 'flight_iata': flight_number}
    
    try:
        response = requests.get('http://api.aviationstack.com/v1/flights', params=params)
        response.raise_for_status()
        data = response.json().get("data", [])
        print(f"🛬 Received data: {data[:1]}")

        if not data:
            return f"No flight data found for IATA code: {flight_number}"
        
        return data[0]
    except Exception as e:
        print(f"❌ Exception: {e}")
        return f"An error occurred while contacting the flight API: {e}"