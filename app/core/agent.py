import os
import ast 
import json
from typing import List
from fastapi import HTTPException
from app.schemas.datamodels import TestCaseIn
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.core.config import GEMINI_API_KEY
from google.api_core.exceptions import ResourceExhausted

from helper.extra import catch_async


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)
parser = JsonOutputParser()

prompt = PromptTemplate.from_template("""
You are an expert API tester.

Given the following API description, generate 3-5 realistic test cases per endpoint.
Each test case should include:
- endpoint
- method (GET/POST/etc.)
- name (short readable title)
- request_body (if applicable, as a JSON object)
- expected_status (e.g., 200, 400, 401)

Return a JSON list of test cases.

API Description:
{api_description}
""")

@catch_async
async def generate_test_cases(api_description: str) -> List[TestCaseIn]:
    chain = prompt | llm | parser
    result = await chain.ainvoke({"api_description": api_description})

    for item in result:
        rb = item.get("request_body")
        if isinstance(rb, str):
            try:
                item["request_body"] = json.loads(rb.replace("'", '"'))
            except json.JSONDecodeError:
                try:
                    item["request_body"] = ast.literal_eval(rb)
                except Exception:
                    item["request_body"] = {}


    test_cases = [TestCaseIn(**item) for item in result]
    return test_cases
