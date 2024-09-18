from pydantic import BaseModel


class Query(BaseModel):
    messages: list[dict[str, str]]
