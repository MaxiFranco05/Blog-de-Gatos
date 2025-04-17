from fastapi import APIRouter, HTTPException
from app.core.database import SessionLocal
from app.models.schema import Post, NewPost, PostSchema, User
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", tags=["Post"]
)

@router.get("/")
def get_all_posts():
    with SessionLocal() as db:
            posts =  db.query(Post).all()
    return {"results": posts}

@router.get("/{id}")
def get_a_post(id: int):
    with SessionLocal() as db:
            post = db.query(Post).filter(Post.id == id).first()
            if not post:
                 raise HTTPException(status_code=404, detail=f"Post #{id} no encontrado.")
    return {"results": post}

@router.post("/new", response_model=PostSchema)
def new_post(post: NewPost):
    with SessionLocal() as db:

        if not db.query(User).filter(User.id == post.author_id).first():
             raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
        new_post = Post(title=post.title, content=post.content, author_id=post.author_id)
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
          return {"result": f"Post #{id} actualizado.", "post": post}