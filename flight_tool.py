import requests

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="flightChecker",stateless_http=True)

@mcp.tool()
def get_flight_info(flight_number):
    
    """
    Retrieves real-time information for a given flight number.

    Args:
        flight_number: The IATA code for the flight (e.g., 'BA2490', 'UA1950').

    Returns:
        A dictionary containing the flight details or a message if not found.
    """

    AVIATIONSTACK_API_KEY = "212ab815742e0de4e062a80f5f5220c3"

    print("Hello from remote-mcp!")
    params = {'access_key': AVIATIONSTACK_API_KEY, 'flight_iata': flight_number}
    try:
        response = requests.get('http://api.aviationstack.com/v1/flights', params=params)
        response.raise_for_status()
        data = response.json().get("data", [])

        if not data:
            return f"No flight data found for IATA code: {flight_number}"
        
        # Return the first, most relevant result
        return data[0]
    except Exception as e:
        return f"An error occurred while contacting the flight API: {e}"