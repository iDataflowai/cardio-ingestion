# src/ingestion/raw_loader.py

from pydantic import BaseModel, Field, validator, root_validator
from typing import Any, Dict


class RawInputSchema(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    sample_id = Field(..., description="Hospital generated sample identifier, must be provided by hospital.")
    trace_id: str | None = Field(None, description="Ignored if provided; ingestion layer generates a new trace_id")

    biomarkers: Dict[str, float | int | str | None] = Field(..., description="Raw biomarker values by hospital")

    metadata: Dict[str, Any] | None = Field(None, description="additional metadata like, gender, age etc")

    @validator('biomarkers')
    def validate_biomarkers(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("biomarkers must be a non-empty dictionary")
        return value

    @root_validator(pre=True)
    def strip_user_trace_id(self, values):
        if "trace_id" in values:
            values["trace_id"] = None
        return values

    class Config:
        extra = "ignore"
