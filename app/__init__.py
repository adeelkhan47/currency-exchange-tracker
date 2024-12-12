import asyncio
from fastapi import FastAPI
from .tasks import schedule_exchange_rate_update  # Importing the function to update exchange rates
from .db import initialize_db  # Importing the function to initialize the database

app = FastAPI()  # Creating an instance of the FastAPI application

# Event triggered on startup
@app.on_event("startup")
async def startup_event():
    initialize_db()  # Initializing the database when the app starts
    # Run the update once on startup
    await schedule_exchange_rate_update()  # Update the exchange rate once when the app starts
    asyncio.create_task(run_periodically())  # Create a task to run periodic updates in the background

# Function to run the exchange rate update periodically
async def run_periodically():
    while True:
        await schedule_exchange_rate_update()  # Update the exchange rate
        await asyncio.sleep(20 * 60)  # Wait for 20 minutes before running again (20 minutes = 20 * 60 seconds)
