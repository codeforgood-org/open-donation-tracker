"""Main FastAPI application"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, donations, organizations, campaigns, impact, admin, files, export, websocket, gamification, social, search, webhooks

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A comprehensive donation tracking platform for transparency and impact visualization",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
import os
if os.path.exists("uploads"):
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(donations.router, prefix="/api")
app.include_router(organizations.router, prefix="/api")
app.include_router(campaigns.router, prefix="/api")
app.include_router(impact.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(files.router, prefix="/api")
app.include_router(export.router, prefix="/api")
app.include_router(websocket.router)  # WebSocket endpoints (no prefix)
app.include_router(gamification.router, prefix="/api")
app.include_router(social.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(webhooks.router, prefix="/api")


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to Open Donation Tracker API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"},
    )


@app.exception_handler(500)
async def server_error_handler(request, exc):
    """Custom 500 handler"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
