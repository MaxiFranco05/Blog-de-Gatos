from fastapi import FastAPI
from app.modules.post.route import router as post_route
from app.modules.users.route import router as user_route
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_route)
app.include_router(user_route)