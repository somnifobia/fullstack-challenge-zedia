from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.routes.dependencies import get_db, get_current_user
from core.templates import render_template
from db.models import Message, User, Template
from schemas.message import MessageCreate, MessageOut
from core.templates import render_template

router = APIRouter()


@router.get("/", response_model=List[MessageOut])
def list_my_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    messages = (
        db.query(Message)
        .filter(Message.recipient_id == current_user.id)
        .order_by(Message.created_at.desc())
        .all()
    )
    return messages


@router.get("/sent", response_model=List[MessageOut])
def list_sent_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    messages = (
        db.query(Message)
        .filter(Message.sender_id == current_user.id)
        .order_by(Message.created_at.desc())
        .all()
    )
    return messages


@router.post(
    "/",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipient = db.query(User).filter(User.email == data.recipient_email).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found",
        )

    subject = ""
    body = ""

    if data.template_id is not None:
        template = (
            db.query(Template)
            .filter(
                Template.id == data.template_id,
                Template.owner_id == current_user.id,
            )
            .first()
        )
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found for this user",
            )

        subject = render_template(template.subject, data.variables)
        body = render_template(template.body, data.variables)
    else:
        # mensagem sem template: subject/body vêm do próprio body, simples
        if not data.variables or "subject" not in data.variables or "body" not in data.variables:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="subject and body required when template_id is not provided",
            )
        subject = data.variables["subject"]
        body = data.variables["body"]

    db_message = Message(
        subject=subject,
        body=body,
        sender_id=current_user.id,
        recipient_id=recipient.id,
        template_id=data.template_id,
        sent_at=datetime.utcnow(),
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    # aqui poderíamos disparar e-mail real; por enquanto só salva no banco
    return db_message


@router.get("/{message_id}", response_model=MessageOut)
def get_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = (
        db.query(Message)
        .filter(
            Message.id == message_id,
            (Message.sender_id == current_user.id)
            | (Message.recipient_id == current_user.id),
        )
        .first()
    )
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    return message
