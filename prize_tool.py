import requests
import os
import io
import csv

# from mcp.server.fastmcp import FastMCP
try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:
    # Try importing from a local path if running locally
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from fastmcp import FastMCP

mcp = FastMCP(name="nobelChecker",stateless_http=True)

@mcp.tool()
def nobel_checker(year, subject):
    """
    Finds the Nobel Prize winner(s) for a given year and subject using the Nobel Prize API.

    Args:
        year (int): The year of the prize.
        subject (str): The category of the prize (e.g., 'physics', 'chemistry', 'peace').

    Returns:
        list: A list of strings, where each string is the full name of a winner.
              Returns an empty list if no prize was awarded or if an error occurred.
    """
    BASE_URL = "http://api.nobelprize.org/v1/prize.csv"
    
    # Prepare the parameters for the request, converting subject to lowercase
    # to match the API's expectation.
    params = {
        'year': year,
        'category': subject.lower()
    }
    
    try:
        # Make the request using the safe 'params' argument
        response = requests.get(BASE_URL, params=params)
        
        # This will raise an exception for bad status codes (like 404 or 500)
        response.raise_for_status()

        # If the API returns no data (e.g., no prize that year), the text will
        # often just be the header row. We check if there's more than one line.
        if len(response.text.splitlines()) <= 1:
            return [] # No winners found

        # Use io.StringIO to treat the response text (a string) like a file
        csv_file = io.StringIO(response.text)
        
        # Use DictReader to easily access columns by name
        reader = csv.DictReader(csv_file)
        
        winners = []
        for row in reader:
            full_name = f"{row['firstname']} {row['surname']}"
            winners.append(full_name)
            
        return winners

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        return [] # Return an empty list on network or HTTP errors
