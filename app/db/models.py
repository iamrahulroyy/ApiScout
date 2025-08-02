from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class TestCase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    endpoint: str
    method: str
    name: str
    request_body: Optional[str] = None
    expected_status: int

    test_plan_id: Optional[int] = Field(default=None, foreign_key="testplan.id")
    result: Optional["TestResult"] = Relationship(back_populates="test_case")


class TestResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    test_case_id: int = Field(foreign_key="testcase.id")
    actual_status: int
    response_body: Optional[str]
    latency_ms: Optional[float]
    success: bool

    test_case: Optional[TestCase] = Relationship(back_populates="result")


class TestPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    test_cases: List[TestCase] = Relationship(back_populates="test_plan")
