from typing import List, Optional
from urllib.parse import parse_qs
from fastapi import APIRouter, FastAPI, HTTPException, Query, Request
import sqlite3

from flask import request

from model.Article import Article
from model.Comment import Comment
from model.Links import Links

app = FastAPI()
api_router = APIRouter(prefix="/v1")
connexion = sqlite3.connect("blog.db", check_same_thread=False)


# ---------------------- SEARCH --------------------
# @api_router.get("/articles/search", status_code=200)
# def search_articles(request: Request, q: str = None):
#     cursor = connexion.cursor()
#     cursor.execute(
#         'SELECT * FROM article WHERE title LIKE :q OR slug LIKE :q OR content LIKE :q OR author LIKE :q;',
#         {"q": '%' + q + '%'}
#     )
#     rows = cursor.fetchall()

#     articles = []
#     for row in rows:
#         articles.append(
#             Article(
#                 article_id=row[0],
#                 title=row[1],
#                 slug=row[2],
#                 content=row[3],
#                 author=row[4]
#             )
#         )
#     return articles

#################### Search correction du prof ####################
# ---------------------- SEARCH --------------------

@api_router.get('/')
def index():
    return {
        "path": "/v1",
        "message": "Bienvenue sur l'API de mon blog"
    }


@api_router.get("/articles/search", status_code=200)
def search_articles(request: Request):
    params = str(request.query_params)
    filtered_params = []
    params_dict = parse_qs(params)

    for param in params_dict:
        if param in ["title", "slug", "content", "author"]:
            filtered_params.append(param)

    like_conditions = ""

    for param in filtered_params:
        like_conditions += f'{param} LIKE "%{params_dict[param][0]}%" OR '

    cursor = connexion.cursor()
    cursor.execute(f"SELECT * FROM article WHERE {like_conditions[:-4]};")
    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append(
            Article(
                article_id=row[0],
                title=row[1],
                slug=row[2],
                content=row[3],
                author=row[4],
            )
        )

    parent = "/v1/articles"
    return {
        "articles": result,
        "_links": Links(self=request.url.path,
        parent= parent)
    }


# route pour recuperer un article
@api_router.get("/articles")
def get_articles(
     request: Request, filter: Optional[List[str]] = Query(None), page: Optional[int] = 1
):
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM article LIMIT 5 OFFSET :offset;", {"offset": (page-1)*5})
    articles = cursor.fetchall()

    result = []
    for article in articles:
        obj_article = Article(
            article_id=article[0],
            title=article[1],
            slug=article[2],
            content=article[3],
            author=article[4],
        )
        if filter:
            result.append(obj_article.model_dump(include=filter))
        else:
            result.append(obj_article)
                
                
        return {
            "articles": result,
            "_links": Links(self=request.url.path,
                            parent="/v1/",
                            prev="/v1/articles?page=" + str(page-1),
                            next="/v1/articles?page=" + str(page+1))
        }   

        # CA C'EST LA VERSION DE NADJIDE
        # parent = "/v1/articles"
        # prev_page = None
        # next_page = page + 1
        # page = page
        # if page < 1:
        #     prev_page = None
        # if page > 1:
        #     prev_page = page - 1
        # if len(articles) == 5:
        #     next_page = page + 1
        # return {
        #     "articles": result,
        #     "_links": Links(self=request.url.path + "?page=" + str(page),
        #     parent= parent,
        #     prev="/v1/articles?page=" + str(prev_page),
        #     next="/v1/articles?page=" + str(next_page))
        # }




@api_router.post("/articles", status_code=201)
def post_article(article: Article):
    cursor = connexion.cursor()
    article_id = cursor.execute(
        "INSERT INTO article (title, slug, content, author) VALUES (:title, :slug, :content, :author);",
        {
            "title": article.title,
            "slug": article.slug,
            "content": article.content,
            "author": article.author,
        },
    ).lastrowid
    connexion.commit()

    return Article(
        article_id=article_id,
        title=article.title,
        slug=article.slug,
        content=article.content,
        author=article.author,
    )


@api_router.get("/articles/{article_id}")
def get_article(article_id: int):
    cursor = connexion.cursor()
    cursor.execute(
        "SELECT * FROM article WHERE article_id = :article_id;",
        {"article_id": article_id},
    )
    article = cursor.fetchone()
    if article is not None:
        return article
    else:
        raise HTTPException(status_code=404, detail="Article inexistant")


@api_router.put("/articles/{article_id}", status_code=200)
def put_article(article_id: int, article: Article):
    cursor = connexion.cursor()
    cursor.execute(
        "UPDATE article SET title = :title, slug = :slug, content = :content, author = :author WHERE article_id = :article_id;",
        {
            "article_id": article_id,
            "title": article.title,
            "slug": article.slug,
            "content": article.content,
            "author": article.author,
        },
    )
    connexion.commit()
    if cursor.rowcount > 0:
        return Article(
            article_id=article_id,
            title=article.title,
            slug=article.slug,
            content=article.content,
            author=article.author,
        )
    else:
        raise HTTPException(status_code=404, detail="Article inexistant")


@api_router.delete("/articles/{article_id}", status_code=204)
def delete_article(article_id: int):
    cursor = connexion.cursor()
    cursor.execute(
        "DELETE FROM article WHERE article_id = :article_id;",
        {"article_id": article_id},
    )
    connexion.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Article inexistant")


######################## COMMENTAIRES ########################


@api_router.get("/articles/{article_id}/comments", status_code=200)
def get_comments(article_id: int):
    cursor = connexion.cursor()
    cursor.execute(
        "SELECT * FROM comment WHERE article_id = :article_id;",
        {"article_id": article_id},
    )
    comments = cursor.fetchall()
    if comments is not None:
        return comments
    else:
        raise HTTPException(status_code=404, detail="Article inexistant")


@api_router.post("/articles/{article_id}/comments", status_code=201)
def post_comment(article_id: int, comment: Comment):
    cursor = connexion.cursor()
    cursor.execute(
        "INSERT INTO comment (title, content, article_id) VALUES (:title, :content, :article_id);",
        {"title": comment.title, "content": comment.content, "article_id": article_id},
    )
    comment_id = cursor.lastrowid
    connexion.commit()

    return Comment(
        comment_id=comment_id,
        title=comment.title,
        content=comment.content,
        article_id=article_id,
    )


app.include_router(api_router)
