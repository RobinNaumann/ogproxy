from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup
import os
import time
from threading import Lock

app = FastAPI()

# Get allowed origins from environment variable
allowed_origins = os.getenv("ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory cache for og: metadata
_og_cache = {}
_og_cache_lock = Lock()
_cache_duration = int(os.getenv("CACHE_MINUTES", "60")) * 60  # minutes to seconds


@app.get("/")
async def root():
    return {
        "message": "Open Graph Metadata Proxy is running.",
        "version": "1.0.0",
        "source": "https://github.com/robinnaumann/ogproxy",
    }


@app.get("/og")
async def get_og_metadata(url: str):
    now = time.time()
    # Check cache
    with _og_cache_lock:
        cached = _og_cache.get(url)
        if cached and now - cached["timestamp"] < _cache_duration:
            return JSONResponse(content=cached["data"])

    # Not cached or expired, fetch
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {e}")

    soup = BeautifulSoup(resp.text, "html.parser")
    og_data = {}
    for tag in soup.find_all("meta"):
        prop = tag.get("property", "")
        # prop may be a list (AttributeValueList) or a string
        if isinstance(prop, list):
            prop = prop[0] if prop else ""
        if isinstance(prop, str) and prop.startswith("og:"):
            og_data[prop.replace("og:", "")] = tag.get("content", "")

    # Store in cache
    with _og_cache_lock:
        _og_cache[url] = {"data": og_data, "timestamp": now}

    return JSONResponse(content={"data": og_data})
