from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.data import get_blog_by_slug, get_published_posts
from app.models import BlogListResponse, BlogPostOut

router = APIRouter()


@router.get("", response_model=BlogListResponse)
def list_blog_posts(db: Session = Depends(get_db)):
    posts = get_published_posts(db)
    return BlogListResponse(
        items=[BlogPostOut.model_validate(p) for p in posts],
        total=len(posts),
    )


@router.get("/{slug}", response_model=BlogPostOut)
def get_blog_post(slug: str, db: Session = Depends(get_db)):
    post = get_blog_by_slug(db, slug)
    if post is None or not post.published:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return BlogPostOut.model_validate(post)
