import contextlib
from fastapi import FastAPI
from temp_tool import mcp as temp_mcp
from prize_tool import mcp as prize_mcp
import os
from dotenv import load_dotenv

load_dotenv()

# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(temp_mcp.session_manager.run())
        await stack.enter_async_context(prize_mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/temp", temp_mcp.streamable_http_app())
app.mount("/prize", prize_mcp.streamable_http_app())

PORT = int(os.getenv("PORT", "10000"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)