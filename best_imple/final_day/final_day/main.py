from fastapi import FastAPI
from Routes import auth_routes, news_routes, external_server_routes, notification_routes, category_routes
from Scheduler.news_sync_scheduler import start_news_sync_scheduler
from config.database import DbConnection

app = FastAPI(title="News Aggregation API", version="1.0.0")

# Create database tables on startup
DbConnection.create_tables()

app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(news_routes.router, prefix="/api/v1")
app.include_router(external_server_routes.router, prefix="/api/v1")
app.include_router(notification_routes.router, prefix="/api/v1")
app.include_router(category_routes.router, prefix="/api/v1")

start_news_sync_scheduler()

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Aggregation API!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "News Aggregation API is running"}