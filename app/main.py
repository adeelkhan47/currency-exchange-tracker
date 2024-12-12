from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI()  # Create an instance of the FastAPI application

# Middleware for CORS (Cross-Origin Resource Sharing) to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],
)

# Include the router from the routes module, which holds your defined API endpoints
app.include_router(router)

# Run the FastAPI app using Uvicorn when the script is run directly
if __name__ == "__main__":
    import uvicorn  # Import Uvicorn to serve the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the app on host 0.0.0.0 and port 8000
