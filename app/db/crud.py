from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import TestPlan, TestCase, TestResult
from app.schemas.datamodels import TestPlanIn, TestCaseIn
from helper.extra import catch_async

@catch_async
async def create_test_plan(db: AsyncSession, plan: TestPlanIn) -> TestPlan:
    db_plan = TestPlan(title=plan.title, description=plan.description)
    db.add(db_plan)
    await db.commit()
    await db.refresh(db_plan)
    return db_plan

@catch_async
async def add_test_cases(db: AsyncSession, plan_id: int, test_cases: list[TestCaseIn]) -> None:
    db_cases = [
        TestCase(
            endpoint=tc.endpoint,
            method=tc.method,
            name=tc.name,
            request_body=tc.request_body if tc.request_body else None,  
            expected_status=tc.expected_status,
            test_plan_id=plan_id
        )
        for tc in test_cases
    ]
    db.add_all(db_cases)
    await db.commit()


@catch_async
async def get_test_plan(db: AsyncSession, plan_id: int) -> TestPlan | None:
    result = await db.exec(select(TestPlan).where(TestPlan.id == plan_id).options(selectinload(TestPlan.test_cases).selectinload(TestCase.result)))
    return result.one_or_none()
