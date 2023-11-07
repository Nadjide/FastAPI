from fastapi.testclient import TestClient
from main import api_router

from model.Article import Article

client = TestClient(api_router)

def test_get_articles():
    response = client.get("/v1/articles")
    assert response.status_code == 200
    
def test_post_article():
    article = Article(
        title="Test Article",
        slug="test-article",
        content="This is a test article.",
        author="Test Author"
    )
    response = client.post("/v1/articles", json=article.model_dump())
    assert response.status_code == 201
    assert response.json()["title"] == article.title
    assert response.json()["slug"] == article.slug
    assert response.json()["content"] == article.content
    assert response.json()["author"] == article.author
    assert response.json()["article_id"] is not None
    
def test_delete_article():
    response = client.delete("/v1/articles/15")
    assert response.status_code == 204
    
def test_put_article():
    article = Article(
        title="Test Article DE PUT",
        slug="test-article",
        content="This is a test article.",
        author="Test Author"
    )
    response = client.put("/v1/articles/16", json=article.model_dump())
    assert response.status_code == 200
    assert response.json()["title"] == article.title
    assert response.json()["slug"] == article.slug
    assert response.json()["content"] == article.content
    assert response.json()["author"] == article.author
    assert response.json()["article_id"] is not None
    