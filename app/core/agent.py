import os
import json
from typing import List
from app.schemas.testcases import TestCaseIn
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.core.config import GEMINI_API_KEY

# Gemini LLM setup
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)
parser = JsonOutputParser()

# Prompt template
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

async def generate_test_cases(api_description: str) -> List[TestCaseIn]:
    chain = prompt | llm | parser
    result = await chain.ainvoke({"api_description": api_description})
    
    test_cases = [TestCaseIn(**item) for item in result]
    return test_cases
