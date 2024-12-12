# Currency Exchange Tracker

This project is a service to fetch, store, and track exchange rates from the European Central Bank (ECB). It compares today's rates with the previous day's rates and calculates the change. The data is stored in DynamoDB, and the service fetches the exchange rates every 20 minutes.

## Features

- Fetches daily exchange rates from the [European Central Bank](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml).
- Following UTC timezone. 
- Stores exchange rates in DynamoDB.
- Compares today's exchange rates with yesterday's rates and calculates the rate change.
- Automatically fetches exchange rates every 20 minutes.
- Provides a REST API to fetch current exchange rates and compare them with the previous day's rates.

## Project Structure

```plaintext
currency-exchange-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI application and routes
│   ├── db.py                 # DynamoDB client and database functions
│   ├── models.py             # Data models and schemas
│   ├── tasks.py              # Background tasks for fetching and storing rates
│   └── schemas.py            # Pydantic models for validation
├── requirements.txt          # Project dependencies
├── Dockerfile                # Docker setup for the project
├── docker-compose.yml        # Docker Compose configuration
├── localstack/
│   ├── cloudformation.yml    # LocalStack CloudFormation configuration for DynamoDB
├── tests/
│   ├── __init__.py
│   └── test_app.py           # Test cases for the application
├── README.md                 # Project documentation
```
## Features

- Fetches daily exchange rates from the [European Central Bank](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml).
- Stores exchange rates in DynamoDB.
- Compares today's exchange rates with yesterday's rates and calculates the rate change.
- Automatically fetches exchange rates every 20 minutes.
- Provides a REST API to fetch current exchange rates and compare them with the previous day's rates.

## Setup and Installation

### Prerequisites

Before setting up the project, ensure that you have the following software installed:

- **Docker**: [Download Docker](https://www.docker.com/products/docker-desktop)
- **Docker Compose**: [Download Docker Compose](https://docs.docker.com/compose/install/)
- **Python 3.8 or higher** (if you want to run the app locally without Docker): [Download Python](https://www.python.org/downloads/)

### 1. Clone the repository

First, clone the project repository from GitHub:

```bash
git clone https://github.com/your-repo/currency-exchange-tracker.git
cd currency-exchange-tracker
```


### 2. Build the Docker images

The project uses Docker to containerize the application. To build the Docker images for the project, run the following command:
```bash
docker-compose build
```

### 3. Start the containers

Once the images are built, you can start the containers in detached mode by running:

```bash
docker-compose up -d
```

### 4. Run the tests

To run the tests, use the following command to execute them inside the container:
```bash
docker-compose run pytest
```

### 5. Stopping the containers

If you need to stop the containers, use the following command:

```bash
docker-compose down
```



## Assumptions

- Exchange Rate Comparison: If the previous day's exchange rate data is not available, the difference is calculated as today's rate minus 0. This ensures that the calculation still occurs even without previous data.
- Periodic Fetching: The application fetches exchange rates every 20 minutes to keep the data updated and relevant.

# API Endpoint: `GET /exchange-rates/current`

## Description
Fetches the current exchange rates from the European Central Bank (ECB) and stores them in DynamoDB for today's date. If today's rates are already present, they will be updated.

## Method
`GET`

## URL
`/exchange-rates/current`

## Response

### Success Response
#### HTTP Status Code: `200 OK`

#### Response Body (JSON)
```json
[
  {
    "currency": "USD",
    "rate": 1.2345
  },
  {
    "currency": "GBP",
    "rate": 0.8765
  }
]
```

# API Endpoint: `GET /exchange-rates/compare`

## Description
Fetches and compares today's exchange rates with the previous day's rates.  
The rate change is calculated as:  
**Rate Change = Today's Rate - Yesterday's Rate**  

If yesterday's rate is unavailable, the rate change is calculated as:  
**Rate Change = Today's Rate - 0**

## Method
`GET`

## URL
`/exchange-rates/compare`

## Response

### Success Response
#### HTTP Status Code: `200 OK`

#### Response Body (JSON)
```json
[
  {
    "currency": "USD",
    "rate": 1.2345,
    "change": 0.1234
  },
  {
    "currency": "GBP",
    "rate": 0.8765,
    "change": -0.0123
  }
]
```