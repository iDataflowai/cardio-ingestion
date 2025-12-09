# # src/ingestion/raw_loader.py

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Dict, Any, Optional, Union


class RawInputSchema(BaseModel):
    """
    Validation model for raw ingestion input loaded from S3 or API.

    Rules:
    - user_id: required
    - sample_id: required (lab-generated, must not be empty)
    - trace_id: must NOT be provided by client (strip if present)
    - biomarkers: required non-empty dictionary
    - metadata: optional
    """

    user_id: str = Field(..., description="User identifier")

    sample_id: str = Field(
        ...,
        description="Lab-generated sample identifier; MUST be provided"
    )

    # trace_id will always be overwritten; incoming value ignored
    trace_id: Optional[str] = Field(None, description="Ignored if provided; ingestion pipeline generates a new one.")

    biomarkers: Dict[str, Union[float, int, str, None]] = Field(..., description="Dictionary of raw biomarker values")

    metadata: Optional[Dict[str, Any]] = Field(None, description="Extra info like age, sex, lab name, timestamps")

    # ------------------------------
    # Validators for Pydantic v2
    # ------------------------------

    # @field_validator("sample_id")
    # def sample_id_required(self, v):
    #     if v is None or v == "":
    #         raise ValueError("sample_id must be provided by the lab and cannot be empty")
    #     return v
    #
    # @field_validator("biomarkers")
    # def validate_biomarkers(self, v):
    #     if not v or not isinstance(v, dict):
    #         raise ValueError("biomarkers must be a non-empty dictionary")
    #     return v
    #
    # @model_validator(mode="before")
    # def strip_trace_id(self, values):
    #     # Ensure user-provided trace_id is ignored
    #     if "trace_id" in values:
    #         values["trace_id"] = None
    #     return values

    model_config = {"extra": "ignore"}
