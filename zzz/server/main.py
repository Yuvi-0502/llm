from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.container import get_container, Container
from app.api.routes import auth, users, articles, external_apis
from app.core.scheduler import start_scheduler

app = FastAPI(
    title="News Aggregation System",
    description="A system for aggregating and categorizing news articles",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(articles.router, prefix="/api/articles", tags=["Articles"])
app.include_router(external_apis.router, prefix="/api/external-apis", tags=["External APIs"])

@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    container = get_container()
    start_scheduler(container.article_service)

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    container = get_container()
    container.cleanup()

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to the News Aggregation System",
        "docs": "/docs",
        "redoc": "/redoc"
    } 