from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlmodel import Field

class TestCaseIn(BaseModel):
    endpoint: str
    method: str
    name: str
    request_body: Optional[Dict[str, Any]] = Field(default_factory=dict)
    expected_status: int

class TestCaseOut(TestCaseIn):
    id: int

class TestResultOut(BaseModel):
    id: int
    test_case_id: int
    actual_status: int
    response_body: Optional[dict]
    latency_ms: Optional[float]
    success: bool

class TestPlanIn(BaseModel):
    title: str
    description: Optional[str] = None
    api_description: str 

class TestPlanOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    test_cases: List[TestCaseOut] = []

