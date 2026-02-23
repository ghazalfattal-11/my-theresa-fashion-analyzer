from pydantic import BaseModel, Field


class AnalysisResponse(BaseModel):
    filename: str
    caption: str
    status: str = "success"


class ErrorResponse(BaseModel):
    detail: str
    status: str = "error"
