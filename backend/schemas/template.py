from datetime import datetime
from pydantic import BaseModel

class TemplateBase(BaseModel):
    name: str
    subject: str
    body:str
    # lista simples de variáveis
    variables: str | None = None

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    name: str | None = None
    subject: str | None = None
    body: str | None = None
    variables: str | None = None

class TemplateOut(TemplateBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True