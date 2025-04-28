from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from openai import OpenAI
from langchain.chains import LLMChain
import os,json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import langchain_community
import re 
load_dotenv()

def process_quota_request(user_input: str) -> dict:
        template = """
You are an assistant that extracts JSON data to help update OpenStack project quotas.
Return a JSON object with keys: action, resource_type, target_project, value.
Examples:
Input: "Set quota for instances in project 'my_project' to 10"
Output: {{ "action": "set_quota", "resource_type": "instances", "target_project": "my_project", "value": 10 }}

Input: {user_input}
Output:
"""

        pt = PromptTemplate(template=template, input_variables=["user_input"])
        llm = ChatOpenAI(
            model="Qwen2.5-14B-Instruct-1M-GGUF",
            temperature=0.7,
            streaming=True,
            openai_api_key="lm-studio",
            openai_api_base="http://10.0.16.150:1234/v1"
        )
        chain = LLMChain(llm=llm, prompt=pt)
        result = chain.run(user_input=user_input)
        json_match = re.search(r'{.*}', result, re.DOTALL)
        if json_match: 
           json_string = json_match.group(0)
           print(f"Extracted JSON string: {json_string}")
        try:
           json_object = json.loads(json_string)
           return json_object
        except json.JSONDecodeError as e:
           print(f"JSONDecodeError: {e.msg} at line {e.lineno} column {e.colno} (char {e.pos})")
           return None
        else:
            print("No JSON found in the input string.")
            return result


