from fastapi import FastAPI, Request
from app.api import auth, course, note
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Study Snipps API",
    description="API for sharing university course notes",
    version="1.0.0",
    docs_url=None #use /docs to get apidocs
)

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth.router, prefix="/api/auth")
app.include_router(course.router, prefix="/api/course")
app.include_router(note.router, prefix="/api/note")

@app.get("/api")
def api_root():
    return {"message": "Welcome to Study Snipps API"}

#frontend stuff

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/course", response_class=HTMLResponse)
async def courses_page(request: Request):
    """All courses page"""
    return templates.TemplateResponse("courses.html", {"request": request})

@app.get("/course/{course_id}", response_class=HTMLResponse)
async def course_detail(request: Request, course_id: str):
    """Single course detail page"""
    return templates.TemplateResponse("course_detail.html", {"request": request, "course_id": course_id})

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    """Upload note page"""
    return templates.TemplateResponse("upload.html", {"request": request})

@app.get("/auth", response_class=HTMLResponse)
async def auth_page(request: Request):
    """Login/Signup page"""
    return templates.TemplateResponse("auth.html", {"request": request})