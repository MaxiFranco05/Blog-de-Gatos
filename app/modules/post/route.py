from fastapi import APIRouter, HTTPException, Query
from app.core.database import SessionLocal
from app.models.schema import Post, NewPost, PostSchema, User
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", tags=["Post"]
)

@router.get("/", response_model=list[PostSchema])
def get_all_posts():
    with SessionLocal() as db:
            posts =  db.query(Post).all()
    return posts

@router.get("/")
def get_posts(page: int = Query(1, ge=1)):
    items= page * 10
    with SessionLocal() as db:
            for i in range(items - 10, items):
                post = db.query(Post).order_by(Post.created_at.desc()).offset(i).first()
                if not post:
                    raise HTTPException(status_code=404, detail=f"Post #{i} no encontrado.")
                user = db.query(User).filter(User.id == post.author_id).first()
                if not user:
                    raise HTTPException(status_code=404, detail=f"Usuario #{post.author_id} no encontrado.")
                result = {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "author_id": post.author_id,
                    "created_at": post.created_at,
                    "last_update": post.last_update,
                    "author": {
                        "id": user.id,
                        "username": user.username,
                        "profile_pic": user.profile_pic
                    }
                }
    return result
@router.get("/{id}")
def get_a_item(id: int):
    with SessionLocal() as db:
            post = db.query(Post).filter(Post.id == id).first()
            if not post:
                 raise HTTPException(status_code=404, detail=f"Post #{id} no encontrado.")
    return post

@router.post("/new", response_model=PostSchema)
def new_post(post: NewPost):
    with SessionLocal() as db:
        if not db.query(User).filter(User.id == post.author_id).first():
             raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        img = post.profile_pic if hasattr(post, "profile_pic") and post.profile_pic else f"https://ui-avatars.com/api/?background=random&name={post.title.replace(' ', '-')}
        new_post = Post(title=post.title, content=post.content, author_id=post.author_id, img=img)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    return new_post
    
@router.delete("/del/{id}", tags=["Delete"])
def delete_post(id: int):
    with SessionLocal() as db:
         post_dl= db.query(Post).filter(Post.id == id).first()
         if not post_dl:
              raise HTTPException(status_code=404, detail=f"Post #{id} no encontrado.")
         db.delete(post_dl)
         db.commit()
    return {"result": f"Post #{id} eliminado satisfactoriamente."}

@router.put("/update/{id}")
def update_post(id: int, post_updt: NewPost):
     with SessionLocal() as db:
          post = db.query(Post).filter(Post.id == id).first()
          if not post:
               raise HTTPException(status_code=404, detail=f"Post #{id} no encontrado.")
          post.title = post_updt.title
          post.content = post_updt.content
          post.author_id = post_updt.author_id
          post.last_update = func.now()
          db.commit()
          db.refresh(post)
          return post