from fastapi import FastAPI
from app.modules.post.route import router as post_route
from app.modules.users.route import router as user_route

tags_metadata = [
    {
        "name": "User",
        "description": "Operaciones relacionadas a usuarios",
    },
    {
        "name": "Post",
        "description": "Operaciones relacionadas a publicaciones",
    },
    {
        "name": "Delete",
        "description": "Operaciones de borrado",
    },
]

app = FastAPI(title="Blog de Gatos",description="API para manejar un blog con FastAPI", version="1.0.0", openapi_tags=tags_metadata)

app.include_router(post_route)
app.include_router(user_route)