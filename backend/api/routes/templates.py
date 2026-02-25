from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.routes.dependencies import get_db, get_current_user
from db.models import Template, User
from schemas.template import TemplateCreate, TemplateOut, TemplateUpdate

router = APIRouter()


@router.get("/", response_model=List[TemplateOut])
def list_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    templates = ( 
        db.query(Template)
        .filter(Template.owner_id == current_user.id)
        .order_by(Template.created_at.desc())
        .all()
    )
    return templates

@router.post(
    "/",
    response_model=TemplateOut,
    status_code=status.HTTP_201_CREATED,
)
def create_template(
    template_in: TemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_template = Template(
        name=template_in.name,
        subject=template_in.subject,
        body=template_in.body,
        variables=template_in.variables,
        owner_id=current_user.id,
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


@router.get("/{template_id}", response_model=TemplateOut)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    template = (
        db.query(Template)
        .filter(
            Template.id == template_id,
            Template.owner_id == current_user.id,
        )
        .first()
    )
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found",
        )
    return template


@router.put("/{template_id}", response_model=TemplateOut)
def update_template(
    template_id: int,
    template_in: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    template = (
        db.query(Template)
        .filter(
            Template.id == template_id,
            Template.owner_id == current_user.id,
        )
        .first()
    )
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found",
        )
    
    data = template_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(template, field, value)

    db.add(template)
    db.commit()
    db.refresh(template)
    return template

@router.delete(
    "/{template_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    template = (
        db.query(Template)
        .filter(
            Template.id == template_id,
            Template.owner_id == current_user.id,
        )
        .first()
    )
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found",
        )
    
    db.delete(template)
    db.commit()
    return None