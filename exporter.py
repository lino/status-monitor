from prometheus_client import start_http_server, Gauge
import requests
import time

# Create a metric to track the status of the website
website_status = Gauge('website_status', 'Status of the website (1=up, 0=down)')

# URL to check
URL = "https://httpstat.us/200"

def check_website():
    try:
        response = requests.get(URL)
        # If the response code is 4xx or 5xx, consider the website down
        if response.status_code >= 400:
            website_status.set(0)
        else:
            website_status.set(1)
    except requests.exceptions.RequestException:
        # If there was an error making the request, consider the website down
        website_status.set(1)

if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        check_website()
    time.sleep(30)  # Check every 30 seconds