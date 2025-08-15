from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, auth, utils

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Weather Auth API")

# CORS (adjust origin to your Vite dev server if needed)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://weather-app-stqa-fa.vercel.app/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "API is running"}

# Example protected route
@app.get("/protected")
def protected_route(current_user = Depends(utils.get_current_user)):
    return {"message": f"Hello, {current_user.email}! You are authorized."}
