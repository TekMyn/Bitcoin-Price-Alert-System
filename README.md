# Bitcoin Price Alert System

![Bitcoin Price Alert System](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)

## Overview

This **Bitcoin Price Alert System** monitors the price of Bitcoin and sends an email alert when the price falls below user-defined thresholds. The system uses the [Gmail API](https://developers.google.com/gmail/api) to send email notifications and the [Mempool API](https://mempool.space/api) to fetch Bitcoin price data.

## Features

- Fetches real-time Bitcoin price
- Alerts via email when the price falls below set thresholds
- Logs price and alert information to a text file
- Scheduled to run periodically (every 10 minutes)

## Getting Started

### Prerequisites

- Python 3.13 or higher
- A Google Cloud project with Gmail API enabled
- OAuth2 credentials for Gmail API

### Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/TekMyn/Bitcoin-Price-Alert-System.git
    cd Bitcoin-Price-Alert-System
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Gmail API Credentials:**

    - Replace `SERVICE_ACCOUNT_FILE` in `main.py` with your OAuth2 credentials file.

### Configuration

1. **Edit `main.py`:**

    Update `SERVICE_ACCOUNT_FILE` with the path to your Gmail API credentials JSON file.

    ```python
    SERVICE_ACCOUNT_FILE = 'path_to_your_credentials_json_file.json'
    ```

2. **Set Up Alerts:**

    Run the script and follow the prompts to set up price alerts and your email address.

    ```bash
    python main.py
    ```

## How It Works

1. **Creates Gmail API Service:**

    ```python
    def create_service():
        # Initialize Gmail API service
    ```

    This function handles authentication and creates a service object to interact with the Gmail API.

2. **Fetch Bitcoin Price from mempool API:**

    ```python
    def fetch_bitcoin_price():
        # Get current Bitcoin price from Mempool API
    ```

    Fetches the current Bitcoin price from the Mempool API.

3. **Check if the alers needs to be sent or not:**

    ```python
    def check_alert(price, alert_levels):
        # Determine if the current price meets any alert thresholds
    ```

    Compares the current Bitcoin price with user-defined alert levels to decide if an alert should be sent.

4. **Send Email Alert:**

    ```python
    def send_email_alert(subject, body, to_email):
        # Send an email notification using Gmail API
    ```

    Constructs and sends an email using the Gmail API if the price meets the alert condition.

5. **Log Price Information:**

    ```python
    def log_price(price, alert_info):
        # Log price and alert information to a text file
    ```

    Logs the price and alert details to `price_log.txt`.

6. **Scheduler:**

    ```python
    def main():
        # Setup alerts and schedule the job
    ```

    Sets up alerts and schedules the job to run every 10 minutes.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
