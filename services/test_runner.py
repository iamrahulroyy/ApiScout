import os
import sys
import time
import json
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db.database import async_session
from app.db.models import TestCase, TestResult


base_url = "http://localhost:8009/api"

async def run_test_case(session: AsyncSession, case: TestCase, base_url: str):
    url = f"{base_url.rstrip('/')}{case.endpoint}"
    method = case.method.upper()
    body = json.loads(case.request_body) if isinstance(case.request_body, str) else case.request_body


    try:
        async with httpx.AsyncClient() as client:
            start = time.perf_counter()
            response = await client.request(method, url, json=body)
            end = time.perf_counter()

        latency = (end - start) * 1000  # in ms
        success = response.status_code == case.expected_status

        result = TestResult(
            test_case_id=case.id,
            actual_status=response.status_code,
            response_body=response.json() if "application/json" in response.headers.get("content-type", "") else None,
            latency_ms=latency,
            success=success
        )
        session.add(result)
        await session.commit()
        print(f"✅ {case.name}: {response.status_code} in {latency:.2f}ms")

    except Exception as e:
        print(f"❌ Failed to run test case {case.id}: {e}")

async def get_all_test_cases(session: AsyncSession):
    result = await session.execute(select(TestCase))
    return result.scalars().all()


async def main():
    async with async_session() as session:
        test_cases = await get_all_test_cases(session)
        print(f"📦 Found {len(test_cases)} test cases.\n")

        for case in test_cases:
            print(f"▶ Running test: {case.name}")
            await run_test_case(session, case, base_url)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
