import os.path
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import schedule
import time
import requests

# scopes requried for gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Replace with the path to your OAuth2 credentials file obtained from google cloud console after enabling the gmail api
SERVICE_ACCOUNT_FILE = 'path_to_your_credential_file.json'

def create_service():
    """
    creates and return a Gmail API service object.
    The function handles OAuth2 authentication and authorization. 
    """
    creds = None
    
    # load existing credentials from token.json if available
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials, it initiates a new authorization flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SERVICE_ACCOUNT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the token.json credentials file for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # create and return the Gmail API service
    return build('gmail', 'v1', credentials=creds)

def fetch_bitcoin_price():
    """
    Fetch the current Bitcoin price in USD from the Mempool API. 
    """
    url = 'https://mempool.space/api/v1/prices'
    response = requests.get(url)
    data = response.json()
    return data['USD']

def check_alert(price, alert_levels):
    """
    Check if the Bitcoin price meets any of the alert conditions. 
    
    Args:
        price (float): The current Bitcoin price. 
        alert_levels (dict): Dictionary of alert levels and thresholds. 
    
    Returns:
        tuple: The alert level and amount if the price is below the threshold, else (None, None). 
    """
    for level, amount in alert_levels.items():
        if price < amount:
            return level, amount
    return None, None

def send_email_alert(subject, body, to_email):
    """
    Send an email alert using the Gmail API.
    
    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.
        to_email (str): The recipient's email address.
    """
    service = create_service()

    # Create the email message
    message = MIMEText(body)
    message['to'] = to_email
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        # Send the email
        send_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f'Message Id: {send_message["id"]}')
    except Exception as e:
        print(f'An error occurred: {e}')

def log_price(price, alert_info):
    """
    Log the Bitcoin price and alert information to a file.
    
    Args:
        price (float): The current Bitcoin price.
        alert_info (str): Information about the alert.
    """
    with open('price_log.txt', 'a') as file:
        file.write(f'Price: ${price}, Alert Info: {alert_info}\n')

def job(alert_levels, email):
    """
    Job function that fetches the Bitcoin price, checks alerts, and sends notifications.
    
    Args:
        alert_levels (dict): Dictionary of alert levels and thresholds.
        email (str): The recipient's email address.
    """
    price = fetch_bitcoin_price()
    print(f'Current Bitcoin price: ${price}')
    
    alert_level, alert_amount = check_alert(price, alert_levels)
    if alert_level:
        subject = f'Price Alert: Bitcoin Price Below {alert_level} Level'
        body = (f'Bitcoin price has dropped below the set level for {alert_level}. '
                f'Current price: ${price}. Alert Level: ${alert_amount}.')
        send_email_alert(subject, body, email)
        log_price(price, f'Alert for {alert_level} level at {alert_amount}')

def setup_alerts():
    """
    Set up user-defined price alerts and return the alert levels and email.
    
    Returns:
        tuple: A dictionary of alert levels and thresholds, and the recipient's email address.
    """
    alert_levels = {}
    while True:
        level = input('Enter a price level in USD to set an alert or type "done" to finish: ')
        if level.lower() == 'done':
            break
        try:
            amount = float(level)
            alert_levels[level] = amount
        except ValueError:
            print('Invalid price level. Please enter a numeric value.')

    email = input('Enter your email address, where you will receive the alerts: ')
    return alert_levels, email

def main():
    """
    Main function to set up the alert system and start scheduling.
    """
    print('Setup your price alerts:')
    alert_levels, email = setup_alerts()

    # Schedule the job to run every 10 minutes
    schedule.every(10).minutes.do(job, alert_levels, email)

    print('Price tracking started. Press Ctrl+C to stop.')
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()

"""
The MIT License (MIT)

Copyright (c) 2024 Jagdish Parmar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
