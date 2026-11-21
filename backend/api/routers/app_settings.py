from fastapi import APIRouter

from api.constants import STATUS_SUCCESS, ErrorMessage, Route, Tag
from api.error_handling import bad_request
from api.schemas import SettingUpdateRequest
from settings.config_manager import load_config, save_setting

router = APIRouter(tags=[Tag.SETTINGS])


@router.get(Route.SETTINGS)
def get_all_settings():
    """Returns all application configuration settings."""
    return load_config()


@router.post(Route.SETTINGS)
def update_setting(payload: SettingUpdateRequest):
    """Updates a specific setting key-value pair."""
    setting_name = payload.key.value
    if not save_setting(setting_name, payload.value):
        raise bad_request(ErrorMessage.SETTING_UPDATE_FAILED.format(key=setting_name))
    return {"status": STATUS_SUCCESS, "key": setting_name, "value": payload.value}