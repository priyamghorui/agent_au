# Use the official Microsoft Playwright image with Python & Chromium pre-installed
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Set the working directory inside the container
WORKDIR /app

# Copy dependency definition
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code into the container
COPY . .

# Expose the FastAPI default port
EXPOSE 8000

# Run Uvicorn using dynamic port binding (compatible with Render's $PORT)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]