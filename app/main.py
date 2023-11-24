from fastapi import FastAPI
from .routes import users, auth, business, category, catalog, certifications, comments, messages, rating
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models

app = FastAPI()

# ************************ CORS ************************
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(business.router)
app.include_router(messages.router)
app.include_router(catalog.router)
app.include_router(certifications.router)
app.include_router(comments.router)
app.include_router(rating.router)
app.include_router(category.router)
