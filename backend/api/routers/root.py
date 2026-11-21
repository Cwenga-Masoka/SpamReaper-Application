from fastapi import APIRouter

from api.constants import WELCOME_MESSAGE, Route, Tag

router = APIRouter(tags=[Tag.GENERAL])


@router.get(Route.ROOT)
def read_root():
    return {"message": WELCOME_MESSAGE}