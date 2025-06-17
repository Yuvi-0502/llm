from fastapi import APIRouter, HTTPException
from app.schemas.article import ArticleCreate, ArticleOut
from app.services.article_service import ArticleService
from typing import List

router = APIRouter(prefix="/articles", tags=["articles"])

@router.post("/", response_model=ArticleOut)
def create_article(article: ArticleCreate):
    service = ArticleService()
    return service.create_article(article)

@router.get("/{article_id}", response_model=ArticleOut)
def get_article(article_id: int):
    service = ArticleService()
    article = service.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.get("/", response_model=List[ArticleOut])
def list_articles():
    service = ArticleService()
    return service.get_all_articles()

@router.delete("/{article_id}", response_model=bool)
def delete_article(article_id: int):
    service = ArticleService()
    return service.delete_article(article_id) 