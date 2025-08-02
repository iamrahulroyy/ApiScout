from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TestCaseIn(BaseModel):
    endpoint: str
    method: str
    name: str
    request_body: Optional[dict] = None
    expected_status: int


class TestCaseOut(TestCaseIn):
    id: int

    class Config:
        orm_mode = True


class TestResultOut(BaseModel):
    id: int
    test_case_id: int
    actual_status: int
    response_body: Optional[dict]
    latency_ms: Optional[float]
    success: bool

    class Config:
        orm_mode = True


class TestPlanIn(BaseModel):
    title: str
    description: Optional[str] = None
    api_description: str  # Raw text or OpenAPI description


class TestPlanOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    test_cases: List[TestCaseOut] = []

    class Config:
        orm_mode = True
