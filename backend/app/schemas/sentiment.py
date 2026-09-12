"""Pydantic request/response schemas for the sentiment API."""
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

ModelName = Literal["rnn", "lstm", "gru"]


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Raw input text to analyze.")
    model: ModelName = Field(..., description="Which model to run: rnn, lstm or gru.")

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be blank")
        return v


class PredictResponse(BaseModel):
    model: str
    sentiment: Literal["Positive", "Negative"]
    probability: float
    confidence: float
    processed_text: str
    model_file: Optional[str] = None


class CompareRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be blank")
        return v


class CompareResultItem(BaseModel):
    model: str
    sentiment: Optional[Literal["Positive", "Negative"]] = None
    probability: Optional[float] = None
    confidence: Optional[float] = None
    processed_text: Optional[str] = None
    available: bool = True
    error: Optional[str] = None


class CompareResponse(BaseModel):
    text: str
    results: List[CompareResultItem]


class ModelAvailability(BaseModel):
    model: str
    model_file_found: bool
    model_file: Optional[str]
    tokenizer_file_found: bool
    tokenizer_file: str
    loaded: bool
    error: Optional[str] = None


class SystemModelsResponse(BaseModel):
    models: List[ModelAvailability]
