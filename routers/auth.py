from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
async def getuser():
    return {"user": "authenticated"}