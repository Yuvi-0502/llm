from fastapi import FastAPI
from app.api.v1 import user, article, category, notification, admin, auth
from app.tasks.news_fetcher import start_news_fetcher
from app.tasks.email_sender import start_email_sender

app = FastAPI(title="News Aggregation API")

@app.on_event("startup")
def startup_event():
    start_news_fetcher()
    start_email_sender()

app.include_router(user.router, prefix="/api/v1")
app.include_router(article.router, prefix="/api/v1")
app.include_router(category.router, prefix="/api/v1")
app.include_router(notification.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Aggregation API!"} 