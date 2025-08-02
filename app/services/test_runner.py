import time
import json
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import TestCase, TestResult


async def run_test_case(session: AsyncSession, case: TestCase, base_url: str):
    url = f"{base_url.rstrip('/')}{case.endpoint}"
    method = case.method.upper()
    body = json.loads(case.request_body) if case.request_body else None

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
            response_body=response.json() if response.headers.get("content-type") == "application/json" else None,
            latency_ms=latency,
            success=success
        )
        session.add(result)
        await session.commit()

    except Exception as e:
        print(f"Failed to run test case {case.id}: {e}")
