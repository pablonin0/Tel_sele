FROM python:3.10

WORKDIR /app

# Copy only requirements first (so dependency layer is cached)
COPY requirements.txt .

# Upgrade pip
RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome dependencies
RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

# Now copy the rest of the source code
COPY . .

CMD ["python", "TelsScrprSelenium.py"]
