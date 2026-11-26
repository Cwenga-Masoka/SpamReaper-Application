from fastapi import APIRouter, Depends

from api.constants import HISTORY_CLEARED_MESSAGE, STATUS_SUCCESS, Route, Tag
from api.dependencies import LOGIN_REQUIRED, get_history_repo
from storage.action_history import ActionHistoryRepository

router = APIRouter(tags=[Tag.HISTORY], dependencies=LOGIN_REQUIRED)


@router.get(Route.HISTORY, response_model=list[dict])
def get_action_history(history_repo: ActionHistoryRepository = Depends(get_history_repo)):
    """Returns all history records with the 30-day Gmail trash countdown."""
    return history_repo.get_action_history()


@router.delete(Route.HISTORY_ITEM)
def delete_history_item(sms_id: str, history_repo: ActionHistoryRepository = Depends(get_history_repo)):
    """Removes a single item from the history log."""
    history_repo.delete_history_record(sms_id)
    return {"status": STATUS_SUCCESS, "sms_id": sms_id}


@router.delete(Route.HISTORY)
def clear_history(history_repo: ActionHistoryRepository = Depends(get_history_repo)):
    """Clears all action history records."""
    history_repo.clear_action_history()
    return {"status": STATUS_SUCCESS, "message": HISTORY_CLEARED_MESSAGE}