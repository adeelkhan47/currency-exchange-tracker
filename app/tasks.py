import requests
import xml.etree.ElementTree as ET
from .db import get_dynamodb_client, DYNAMODB_TABLE
from datetime import date, timedelta

# Function to fetch exchange rates from the European Central Bank (ECB)
def fetch_exchange_rates():
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    response = requests.get(url)  # Send request to get the XML data
    response.raise_for_status()  # Raise an error if the request failed

    namespace = {'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
    tree = ET.fromstring(response.content)  # Parse the XML response

    rates = {}
    # Extract currency and rate from the XML
    for cube in tree.findall(".//ns:Cube[@currency]", namespace):
        currency = cube.attrib["currency"]
        rate = float(cube.attrib["rate"])
        rates[currency] = rate
    return rates

# Function to store fetched exchange rates in DynamoDB
def store_exchange_rates(rates):
    client = get_dynamodb_client()
    today = date.today().isoformat()  # Get today's date in ISO format
    for currency, rate in rates.items():
        # Insert each currency rate for today into DynamoDB
        client.put_item(
            TableName=DYNAMODB_TABLE,
            Item={
                "currency": {"S": currency},
                "date": {"S": today},
                "rate": {"N": str(rate)}
            }
        )

# Async function to fetch and store exchange rates periodically
async def schedule_exchange_rate_update():
    rates = fetch_exchange_rates()  # Fetch the latest exchange rates
    store_exchange_rates(rates)  # Store the fetched rates in DynamoDB
