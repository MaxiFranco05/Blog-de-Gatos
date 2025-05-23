from fastapi import APIRouter, HTTPException
from app.models.schema import User, UserSchema, NewUser, AuthUser
from app.core.database import SessionLocal
from typing import List
from app.core.auth import hash_pswrd, auth_pass
from sqlalchemy import func

router = APIRouter(
    prefix="/users", tags=["User"]
    )

@router.get("/", response_model=List[UserSchema])
def get_all_users():
    with SessionLocal() as db:
        users = db.query(User).all()
    return users

@router.get("/{id}", response_model=UserSchema)
def get_a_user(id: int):
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user

@router.post("/signup", response_model=UserSchema)
def new_user(user: NewUser):
    with SessionLocal() as db:
        existing_user = db.query(User).filter((User.username == user.username) or (User.email == user.email)).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="El nombre de usuario o correo ya está en uso.")
        pass_hash = hash_pswrd(user.password)
        profile_pic = user.profile_pic if hasattr(user, "profile_pic") and user.profile_pic else f"https://api.dicebear.com/9.x/micah/svg?seed={user.username}&backgroundType=gradientLinear&facialHairProbability=25&backgroundColor=ffdfbf,ffd5dc,d1d4f9,c0aede,b6e3f4"
        new_user = User(username= user.username, email= user.email, password= pass_hash, profile_pic=profile_pic)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return new_user

@router.delete("/del/{id}", tags=["Delete"])
def delete_user(id: str, user: AuthUser):
    with SessionLocal() as db:
        del_user = db.query(User).filter(id == User.id).first()
        if not del_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        if (user.username == del_user.username) and (auth_pass(user.password, del_user.password)):
            db.delete(del_user)
            db.commit()
        else:
            raise HTTPException(status_code=409, detail="Usuario o contraseña incorrecto.")
        return {"result": f"Usuario #{id} eliminado."}
    
@router.put("/update/{id}")
def update_user(id: str, user_auth: AuthUser,user_updt: NewUser):
    with SessionLocal() as db:
        user = db.query(User).filter(id == User.id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        if (user_auth.username == user.username) and (auth_pass(user_auth.password, user.password)):
            user.username = user_updt.username
            user.email = user_updt.email
            user.password = hash_pswrd(user_updt.password)
            user.last_update = func.now()
            db.commit()
            db.refresh(user)
        else:
            raise HTTPException(status_code=409, detail="Validación errónea, ingrese otro usuario y contraseña.")
        return {"result":f"Usuario #{id} actualizado.","usuario": user}