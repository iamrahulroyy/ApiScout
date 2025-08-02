from fastapi import APIRouter, HTTPException, Depends
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import async_session
from app.schemas.testcases import TestPlanIn, TestPlanOut
from app.core.agent import generate_test_cases
from app.db import crud

router = APIRouter()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

@router.post("/upload-api-doc", response_model=TestPlanOut)
async def upload_api_doc(
    plan: TestPlanIn,
    db: AsyncSession = Depends(get_session)
):
    test_plan = await crud.create_test_plan(db, plan)
    test_cases = await generate_test_cases(plan.api_description)
    await crud.add_test_cases(db, test_plan.id, test_cases)
    db_plan = await crud.get_test_plan(db, test_plan.id)
    return db_plan

@router.get("/get-results/{plan_id}", response_model=TestPlanOut)
async def get_results(
    plan_id: int,
    db: AsyncSession = Depends(get_session)
):
    plan = await crud.get_test_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Test plan not found")
    return plan
