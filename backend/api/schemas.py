from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from api.constants import EditableSetting


class ImmutableModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class EmailIdsRequest(ImmutableModel):
    email_ids: list[str] = Field(min_length=1)


class SettingUpdateRequest(ImmutableModel):
    key: EditableSetting
    value: Any


class CamelCaseResponse(ImmutableModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class SpamEmailResponse(CamelCaseResponse):
    id: str
    sender_name: str
    sender_address: str
    subject: str
    preview: str
    days_left: int