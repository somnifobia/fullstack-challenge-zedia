from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import auth, users, templates, messages
from db.session import engine, Base

app = FastAPI(
    title="Mensageiro API",
    version="0.1.0",
    description="API do desafio full stack"
)

origins = ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(templates.router, prefix="/templates", tags=["templates"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    # importa models para registrar no Base.metadata
    from db import models # noqa: F401
    
    Base.metadata.create_all(bind=engine)