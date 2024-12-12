import os
import boto3  # Importing the boto3 library to interact with AWS services
from botocore.exceptions import NoCredentialsError  # Importing exception handling for missing credentials

DYNAMODB_TABLE = "ExchangeRates"  # Define the DynamoDB table name

# Function to get a DynamoDB client with specific configurations
def get_dynamodb_client():
    endpoint_url = f"http://localstack:4566"  # Endpoint for local DynamoDB (using LocalStack for local testing)
    return boto3.client(
        "dynamodb",  # Specify DynamoDB as the service to interact with
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),  # Get AWS access key from environment or default to 'test'
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),  # Get AWS secret access key from environment or default to 'test'
        region_name=os.getenv("AWS_REGION", "us-east-1"),  # Get AWS region from environment or default to 'us-east-1'
        endpoint_url=endpoint_url  # Set the endpoint URL to LocalStack for local testing
    )

# Function to initialize the DynamoDB database by creating a table
def initialize_db():
    client = get_dynamodb_client()  # Get the DynamoDB client
    try:
        # Create a new DynamoDB table with the defined schema

        client.create_table(
            TableName=DYNAMODB_TABLE,  # Set the table name
            KeySchema=[  # Define the key schema with a partition key and sort key
                {"AttributeName": "currency", "KeyType": "HASH"},  # Partition key (HASH)
                {"AttributeName": "date", "KeyType": "RANGE"}  # Sort key (RANGE)
            ],
            AttributeDefinitions=[  # Define the attributes for the keys
                {"AttributeName": "currency", "AttributeType": "S"},  # 'currency' attribute of type String (S)
                {"AttributeName": "date", "AttributeType": "S"}  # 'date' attribute of type String (S)
            ],
            ProvisionedThroughput={  # Define read and write throughput capacity for the table
                "ReadCapacityUnits": 5,  # Number of read capacity units
                "WriteCapacityUnits": 5  # Number of write capacity units
            }
        )
    except client.exceptions.ResourceInUseException:
        # Catch the exception if the table already exists
        print("Table already exists.")  # Print a message if the table is already created
