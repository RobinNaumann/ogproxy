# OG Proxy

A simple proxy server to fetch and cache Open Graph metadata from URLs, with CORS support.

## Features

- Fetches Open Graph metadata from provided URLs.
- Caches metadata for a configurable duration to reduce load times.
- Supports CORS with configurable allowed origins.

## Configuration

- `ORIGINS`: Comma-separated list of allowed origins for CORS (default: `*`).
- `CACHE_MINUTES`: Duration in minutes to cache the Open Graph metadata (default: `60`).

## Usage

1. Build the Docker image:
   ```bash
   docker build -t ogproxy .
   ```
2. Run the Docker container:
   ```bash
   docker run -d -p 8000:80 -e ORIGINS="*" -e CACHE_MINUTES=60 ogproxy
   ```
3. Access the API endpoint:
   `http://localhost:8000/og?url={TARGET_URL}`
   Replace `{TARGET_URL}` with the URL you want to fetch Open Graph metadata from.
