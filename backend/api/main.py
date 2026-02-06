"""
FastAPI application initialization and configuration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from backend.core.config import get_settings
from backend.api.routes import incident, health

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting InfraMind API...")
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"Using Gemini model: {settings.gemini_model}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down InfraMind API...")


# Create FastAPI application
app = FastAPI(
    title="InfraMind API",
    description="AI-powered infrastructure debugging and root cause analysis",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(incident.router, prefix="/api/v1", tags=["incidents"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "InfraMind API",
        "version": "1.0.0",
        "description": "AI-powered infrastructure debugging",
        "docs": "/docs"
    }
