from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes

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
