Implementation of a remote MCP server that serves two useful tool calling functions.

One gets the latest stock price for a given ticker, and the other retrieves flight information from a given flight number.


To test these out, you can use the following curl commands.

e.g get the latest information for flight BA 1435

$ curl -sN -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_flight_info","arguments":{"flight_number":"BA1435"}}}' https://remote-mcp-syp1.onrender.com/flight/mcp/ |  sed -n '/^data:/{s/^data: //;p}'

Or...

e.g get the latest price of Microsoft

$ curl  -sN   -H 'Content-Type: application/json'   -H 'Accept: application/json, text/event-stream'   -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"stock_price","arguments":{"ticker":"MSFT"}}}'   https://remote-mcp-syp1.onrender.com/stock/mcp/ | sed -n '/^data:/{s/^data: //;p}'

The above commands should work on Linux and WSL2 for Windows

Note: If running these on bare Windows, you may need to add the following flag to ensure correct operation.

curl --ssl-no-revoke  etc...
