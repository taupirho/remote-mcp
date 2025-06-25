import contextlib
from fastapi import FastAPI
from stock_tool import mcp as stock_mcp
from flight_tool import mcp as flight_mcp
import os


# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(stock_mcp.session_manager.run())
        await stack.enter_async_context(flight_mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/stock", stock_mcp.streamable_http_app())
app.mount("/flight", flight_mcp.streamable_http_app())

PORT = os.environ.get("PORT", 10000)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
