from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Dict, Any, Optional, Union


class BiomarkerValueSchema(BaseModel):
    raw_value: Union[float, int, Dict[str, float]]
    raw_unit: str
    is_range: bool
    comment: Optional[str] = ""

    @field_validator("raw_value")
    def validate_raw_value(cls, v, info):
        is_range = info.data.get("is_range", False)

        if is_range:
            if not isinstance(v, dict) or "min" not in v or "max" not in v:
                raise ValueError("Range biomarkers require raw_value={min,max}")
        else:
            if not isinstance(v, (int, float)):
                raise ValueError("raw_value must be numeric when is_range=false")

        return v


class RawInputSchema(BaseModel):
    user_id: str
    sample_id: str
    trace_id: Optional[str] = None
    biomarkers: Dict[str, BiomarkerValueSchema]
    metadata: Optional[Dict[str, Any]] = None

    @model_validator(mode="before")
    def strip_trace_id(cls, data):
        if isinstance(data, dict):
            data = data.copy()
            data["trace_id"] = None   # always override
        return data

    model_config = {"extra": "ignore"}
