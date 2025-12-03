from fastapi import FastAPI
from app.api import auth

app = FastAPI(
    title="Study Snippets API",
    description="API for sharing university course notes",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to Study Snippets API"}