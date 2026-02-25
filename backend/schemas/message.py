from datetime import datetime
from pydantic import BaseModel, EmailStr


class MessageBase(BaseModel):
    subject: str
    body: str


class MessageCreate(BaseModel):
    recipient_email: EmailStr
    template_id: int | None = None
    # valores para substituir nas variáveis do template
    variables: dict[str, str] | None = None


class MessageOut(MessageBase):
    id: int
    sender_id: int
    recipient_id: int
    template_id: int | None = None
    created_at: datetime
    sent_at: datetime | None = None

    class Config:
        from_attributes = True
