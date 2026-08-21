from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine, Base
from app.routers import candidates, ai, company, jobs

# Create database tables (in production, use alembic migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Recruitment Assistant (ARA)")
app.include_router(candidates.router)
app.include_router(ai.router)
app.include_router(company.router)
app.include_router(jobs.router)
app.add_middleware(
    CORSMiddleware,
    # explicitly allowing frontend URL for dev
    allow_origins=["*", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to AI Recruitment Assistant API"}
