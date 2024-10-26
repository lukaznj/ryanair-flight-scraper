# Use an official Python runtime as a parent image
FROM python:3.12.7-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system libraries and tools
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    chromium \
    chromium-driver \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports for the Streamlit app and any other services
EXPOSE 8501
EXPOSE 80

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run supervisord to manage both processes
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]