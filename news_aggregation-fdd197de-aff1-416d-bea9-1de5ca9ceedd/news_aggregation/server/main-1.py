from fastapi import FastAPI
from server.routes import auth_routes, news_routes, user_routes, external_server_routes, category_routes

app = FastAPI(
    title="News Aggregation",
    description="A RESTful API for news aggregation"
)

app.include_router(auth_routes.router)
app.include_router(news_routes.router)
app.include_router(user_routes.router)
app.include_router(external_server_routes.router)
app.include_router(category_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Aggregation API!"}