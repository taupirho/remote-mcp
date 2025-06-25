import yfinance as yf
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="stockChecker", stateless_http=True)

@mcp.tool()
def stock_price(ticker: str): # Renamed for clarity
    """Retrieves the latest stock price for a given ticker symbol."""
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        if 'regularMarketPrice' not in stock_info or stock_info['regularMarketPrice'] is None:
            return {"ticker": ticker, "error": "Ticker symbol not found or data is unavailable."}
        return {
            "ticker": ticker.upper(),
            "company_name": stock_info.get('shortName', 'N/A'),
            "latest_price": stock_info.get('regularMarketPrice', 'N/A')
        }
    except Exception as e:
        return {"ticker": ticker, "error": f"An unexpected error occurred with yfinance: {e}"}