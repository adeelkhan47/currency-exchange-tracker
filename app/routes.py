import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException
from .db import get_dynamodb_client, DYNAMODB_TABLE
from datetime import date, timedelta

from .schemas import ExchangeRateSchema, ExchangeRateSchemaChanges
from .tasks import fetch_exchange_rates

router = APIRouter()


# Endpoint to fetch and update current exchange rates
@router.get("/exchange-rates/current", response_model=list[ExchangeRateSchema])
def update_and_get_current_exchange_rates():
    client = get_dynamodb_client()
    today = date.today().isoformat()

    # Fetch exchange rates from an external service
    try:
        rates = fetch_exchange_rates()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch exchange rates: {str(e)}")

    # Store the rates for today in DynamoDB
    for currency, rate in rates.items():
        client.put_item(
            TableName=DYNAMODB_TABLE,
            Item={
                "date": {"S": today},
                "currency": {"S": currency},
                "rate": {"N": str(rate)}
            }
        )

    # Retrieve today's exchange rates from DynamoDB
    today_rates = client.scan(
        TableName=DYNAMODB_TABLE,
        FilterExpression="#date = :date",
        ExpressionAttributeNames={"#date": "date"},
        ExpressionAttributeValues={":date": {"S": today}}
    )["Items"]

    # Format and sort the response by currency
    response = [{
        "currency": rate["currency"]["S"],
        "rate": float(rate["rate"]["N"])
    } for rate in today_rates]
    response = sorted(response, key=lambda x: x["currency"])
    return response


# Endpoint to fetch and compare exchange rates with the previous day
@router.get("/exchange-rates/compare", response_model=list[ExchangeRateSchemaChanges])
def get_exchange_rates_with_comparison():
    client = get_dynamodb_client()
    current_date = datetime.datetime.now(ZoneInfo("UTC")).date()
    today = current_date.isoformat()
    yesterday = (current_date - timedelta(days=1)).isoformat()

    # Fetch and store today's exchange rates
    rates = fetch_exchange_rates()
    for currency, rate in rates.items():
        client.put_item(
            TableName=DYNAMODB_TABLE,
            Item={
                "date": {"S": today},
                "currency": {"S": currency},
                "rate": {"N": str(rate)}
            }
        )

    # Retrieve today's exchange rates
    today_rates = client.scan(
        TableName=DYNAMODB_TABLE,
        FilterExpression="#date = :date",
        ExpressionAttributeNames={"#date": "date"},
        ExpressionAttributeValues={":date": {"S": today}}
    )["Items"]

    # Retrieve yesterday's exchange rates
    yesterday_rates = client.scan(
        TableName=DYNAMODB_TABLE,
        FilterExpression="#date = :date",
        ExpressionAttributeNames={"#date": "date"},
        ExpressionAttributeValues={":date": {"S": yesterday}}
    )["Items"]
    yesterday_map = {item["currency"]["S"]: float(item["rate"]["N"]) for item in yesterday_rates}

    # Compare today's rates with yesterday's
    response = []
    for rate in today_rates:
        currency = rate["currency"]["S"]
        today_rate = float(rate["rate"]["N"])
        change = today_rate - yesterday_map.get(currency, 0)
        response.append({
            "currency": currency,
            "rate": today_rate,
            "change": change
        })

    # Sort the response by currency
    response = sorted(response, key=lambda x: x["currency"])
    return response
