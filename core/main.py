from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes
from users.routes import router as users_routes
from auth.token_auth import get_authenticated_user
from users.models import UserModel

tags_metadata = [
    {
        "name": "tasks",
        "description": "Operations related to task management",
        "externalDocs": {
            "description": "More about tasks",
            "url": "http://example.com/docs/tasks"
        }
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Applicaton shutdown")

app = FastAPI(title="Todo Application",
              description="This is a Todo application with FastAPI",
              version="0.0.1",
              contact={"name": "Mahtab Babaei",
                       "url": "https://github.com/mahtab-babaei",
                       "email": "mahtaab.babaei@gmail.com"
                       },
              lifespan=lifespan,
              openapi_tags=tags_metadata
              )

app.include_router(tasks_routes)
app.include_router(users_routes)


@app.get("/public")
def public_route():
    return {"message": "this is a public route"}


@app.get("/private")
def private_route(user: UserModel = Depends(get_authenticated_user)):
    print(user.username)
    return {"message": "this is a private route"}
