from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
def read_me():
    #placeholder JWT
    return {"message": "not implemented yet"}