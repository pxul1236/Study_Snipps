from fastapi import FastAPI
from app.api import auth, course

app = FastAPI(
    title="Study Snipps API",
    description="API for sharing university course notes",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)
app.include_router(course.router)

@app.get("/")
def root():
    return {"message": "Welcome to Study Snipps API"}