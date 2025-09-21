FROM python:3.10

WORKDIR /app

# Copy only requirements first (so dependency layer is cached)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome dependencies

RUN apt-get update; apt-get clean

# Add a user for running applications.
RUN apt-get update && apt-get install -y wget unzip \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get -f install -y \
    && rm google-chrome-stable_current_amd64.deb \
    && apt-get clean

RUN echo "Chrome: " && google-chrome --version


COPY . .

CMD ["python", "TelsScrprSelenium.py"]
