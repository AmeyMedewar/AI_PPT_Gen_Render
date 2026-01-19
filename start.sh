#!/bin/bash

# Use Render's PORT environment variable
PORT=${PORT:-10000}

# Start Uvicorn on port 8000 in the background
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &

# Wait a moment for Uvicorn to start
sleep 2

# Start Streamlit on Render's assigned PORT (this will be the public-facing service)
streamlit run src/UI/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.enableCORS false --server.enableXsrfProtection false