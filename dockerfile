FROM python:3.10

WORKDIR /app

# Copy only requirements first (so dependency layer is cached)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome dependencies

RUN apt-get update; apt-get clean

# Add a user for running applications.
# Install chrome for python selenium
RUN apt -f install -y
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y --fix-missing

COPY . .

CMD ["python", "TelsScrprSelenium.py"]
