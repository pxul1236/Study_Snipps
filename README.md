# Study Snippets

> A clean, minimalist platform for university students to share and discover course notes.

**Live Demo:** [https://study-snipps.onrender.com/](https://study-snipps.onrender.com/)

---

## What is this?

A simple place where students can upload and share their course notes without all the bloat of traditional LMS platforms.

No fancy features. No complicated UI. Just notes, courses, and students helping each other out.

---

## Features

-  **User Authentication** - Secure signup/login with JWT tokens
-  **Admin System** - Admins manage courses, students share notes
-  **Course Management** - Browse courses by department, semester, or search
-  **Note Uploads** - Share your handwritten or typed notes with others
-  **Smart Search** - Find notes by course, title, or content
-  **Fast API** - Built with FastAPI for blazing-fast performance

---

## Tech Stack

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [Alembic](https://alembic.sqlalchemy.org/) - Database migrations
- [PostgreSQL](https://www.postgresql.org/) - Relational database
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation

**Security:**
- JWT tokens for authentication
- Argon2 password hashing
- Role-based access control (Admin/Student)

**Frontend:**
- Vanilla HTML/CSS/JavaScript
- No frameworks - just clean, semantic markup
- Responsive design

**Deployment:**
- [Render](https://render.com/) - Web service hosting
- [Supabase](https://supabase.com/) - PostgreSQL database

---

### Prerequisites

- Python 3.10 or higher
- PostgreSQL (or use Supabase/Neon)
- Git

### Local Setup

1. **Clone the repository**
```bash
   git clone https://github.com/pxul1236/Study_Snipps.git
   cd Study_Snipps
```

2. **Create virtual environment**
```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
```env
   DATABASE_URL=postgresql://user:password@localhost:5432/study_snippets
   SECRET_KEY=your-super-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ENVIRONMENT=development
```

   **Generate a secure SECRET_KEY:**
```bash
   python -c "import secrets; print(secrets.token_hex(32))"
```

5. **Set up the database**
```bash
   # Create database (if using local PostgreSQL)
   createdb study_snippets
   
   # Run migrations
   alembic upgrade head
```

6. **Run the application**
```bash
   uvicorn app.main:app --reload
```

7. **Open your browser**
   
   Navigate to: `http://127.0.0.1:8000`
   
   API docs: `http://127.0.0.1:8000/docs`

---

## Usage

### For Students:

1. **Sign up** - Create an account at `/auth`
2. **Browse courses** - Check out available courses
3. **View notes** - Click on any course to see shared notes
4. **Upload notes** - Share your own notes to help others

### For Admins:

1. **Create courses** - Add new courses via API (use `/docs`)
2. **Manage content** - Edit or delete courses and notes
3. **Monitor platform** - Keep things organized and spam-free

### Creating Your First Admin:

Since the `/register-admin` endpoint is disabled for security:

**Option 1: Database method**
```sql
-- In your database (pgAdmin, Supabase SQL Editor, etc.)
UPDATE users SET is_admin = true WHERE email = 'your-email@example.com';
```

**Option 2: Temporary endpoint**
- Uncomment `/register-admin` in `app/api/auth.py`
- Create your admin account
- Comment it back out and redeploy

---

## Project Structure
```
Study_Snipps/
├── app/
│   ├── api/              # API route handlers
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── course.py     # Course management
│   │   └── note.py       # Note management
│   ├── models/           # SQLAlchemy database models
│   │   ├── user.py
│   │   ├── course.py
│   │   └── note.py
│   ├── schemas/          # Pydantic validation schemas
│   ├── utils/            # Helper functions
│   ├── database.py       # Database connection
│   └── main.py           # FastAPI app entry point
├── static/               # CSS, JS, images
├── templates/            # HTML templates
├── alembic/              # Database migrations
├── .env                  # Environment variables (not in git)
├── .env.example          # Template for .env
├── requirements.txt      # Python dependencies
└── README.md
```

---

## Security Features

- ✅ **Password hashing** with Argon2 (industry standard)
- ✅ **JWT authentication** with token expiry
- ✅ **Owner-based authorization** (users can only edit their own content)
- ✅ **Admin-only endpoints** for sensitive operations
- ✅ **Input validation** with Pydantic schemas
- ✅ **SQL injection prevention** through ORM
- ✅ **Environment variable protection** (secrets not in code)

---

## Known Issues

- File uploads currently require external hosting (Google Drive, Imgur, etc.)
- No email verification yet
- Search is basic 
- Mobile UI could use some polish

---


## Contributing

This is a learning project, but contributions are welcome! If you want to add features or fix bugs:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/cool-feature`)
3. Commit your changes (`git commit -m 'Add cool feature'`)
4. Push to the branch (`git push origin feature/cool-feature`)
5. Open a Pull Request

---

## API Documentation

Once running, visit `/docs` for interactive API documentation (Swagger UI).

**Main endpoints:**

- `POST /api/auth/register` - Create new account
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info
- `GET /api/course/` - List all courses
- `POST /api/course/` - Create course (admin only)
- `GET /api/note/` - List all notes
- `POST /api/note/` - Upload a note

---


**Built with ☕ by a student, for students.**
