from pydantic import BaseModel, field_validator


class PuzzleRequest(BaseModel, str_strip_whitespace=True):
    name: str
    size: int

    @field_validator("size")
    @classmethod
    def ensure_size(cls, v: int) -> int:
        if v < 1:
            raise ValueError('"size" must be greater than 0')

        return v
