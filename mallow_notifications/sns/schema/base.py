from typing import Any, Dict, Optional, Union, get_origin

from pydantic import BaseModel, Field

from mallow_notifications.base.exceptions import NotificationError


class BaseSchema(BaseModel):
    def model_dump_without_none(self):
        return {key: value for key, value in self.model_dump().items() if value is not None}

    @classmethod
    def process_input(cls, input_data: Union[BaseModel, Dict[str, any]]) -> dict:

        if isinstance(input_data, cls):
            return input_data.model_dump_without_none()
        elif isinstance(input_data, dict):
            # If it's a dictionary, create an instance of the pydantic model to validate the data
            instance = cls(**input_data)
            return instance.model_dump_without_none()
        else:
            raise NotificationError(f"Invalid type for input_data: {type(input_data)}")

    class Config:
        populate_by_name = True


class NextToken(BaseSchema):
    NextToken: Optional[str] = Field(default=None, alias="next_token")
