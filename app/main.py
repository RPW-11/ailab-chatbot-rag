from fastapi import FastAPI
from app.config import settings
from app.api.v1.routes import routers as v1_routers
from app.lifespan import lifespan

class AppCreator:
    def __init__(self):
        self.app = FastAPI(
            title=settings.APP_NAME,
            description="A chatbot application for AI Robotics Lab",
            version=settings.APP_VERSION,
            lifespan=lifespan,
        )

        @self.app.get("/")
        def root():
            return {"message": "Welcome to the Chatbot App!"}

        self.app.include_router(v1_routers, prefix=settings.API_V1_PREFIX)


app_creator = AppCreator()
app = app_creator.app