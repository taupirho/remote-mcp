import requests
from dotenv import load_dotenv
import os

# from mcp.server.fastmcp import FastMCP
try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:
    # Try importing from a local path if running locally
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from fastmcp import FastMCP
load_dotenv()

mcp = FastMCP(name="flightChecker",stateless_http=True)

@mcp.tool()
def get_flight_info(flight_number):
    print(f"✈️ Tool called with flight number: {flight_number}")
    
    AVIATIONSTACK_API_KEY = os.environ.get("AVIATIONSTACK_API_KEY")
    if not AVIATIONSTACK_API_KEY:
        print("❌ API key not found in environment!")
        return "API key not found."

    print(f"🔐 API key starts with: {AVIATIONSTACK_API_KEY[:5]}...")

    params = {'access_key': AVIATIONSTACK_API_KEY, 'flight_iata': flight_number}
    try:
        response = requests.get('http://api.aviationstack.com/v1/flights', params=params)
        response.raise_for_status()
        data = response.json().get("data", [])

        print(f"📦 API returned {len(data)} records")

        if not data:
            return f"No flight data found for IATA code: {flight_number}"
        
        return data[0]
    except Exception as e:
        print(f"❌ Exception during API call: {e}")
        return f"An error occurred while contacting the flight API: {e}"
    
    @mcp.tool()
    def ping():
        print("✅ ping() tool was called")
        return "pong from Render"