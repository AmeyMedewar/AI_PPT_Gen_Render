# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /src

# Install system dependencies (if needed for your project)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose ports (8000 for Uvicorn, 8501 for Streamlit)
EXPOSE 8000 8501

# Create a startup script
COPY start.sh .
RUN chmod +x start.sh

# Run the startup script
CMD ["./start.sh"]