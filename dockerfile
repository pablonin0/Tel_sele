# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy only requirements first (cache layer)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Install Chrome and dependencies properly
RUN apt-get update && apt-get install -y \
        wget \
        gnupg \
        unzip \
        curl \
        ca-certificates \
        fonts-liberation \
        libappindicator3-1 \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libcups2 \
        libdbus-1-3 \
        libdrm2 \
        libgbm1 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libx11-xcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        xdg-utils \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && ln -s /usr/bin/google-chrome-stable /usr/bin/google-chrome \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the source code
COPY . .

# Set Chrome options for headless use in Docker
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome

# Run your Selenium script
CMD ["python", "TelsScrprSelenium.py"]
