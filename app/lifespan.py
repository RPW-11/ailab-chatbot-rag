from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infrastructure import load_infrastructure, unload_infrastructure

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    This function is called when the application starts up and shuts down.
    """
    await load_infrastructure()

    yield

    await unload_infrastructure()
    
    # Cleanup code can be added here if needed
    print("Application shutting down...")