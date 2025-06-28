from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from transformers import pipeline

generator = pipeline("text2text-generation", model="google/flan-t5-base", max_new_tokens=512)

llm = HuggingFacePipeline(pipeline=generator)

SUMMARY_TEMPLATE = """
Given the following government scheme text, extract the following details:
1. Scheme Benefits
2. Eligibility Criteria
3. Documents Required
4. Application Process

Text:
{text}

Respond in the following format:

### Scheme Benefits:
...

### Eligibility Criteria:
...

### Documents Required:
...

### Application Process:
...
"""

prompt = PromptTemplate(input_variables=["text"], template=SUMMARY_TEMPLATE)
chain = LLMChain(llm=llm, prompt=prompt)

def generate_summary(text: str) -> str:
    try:
        return chain.run(text[:3000])
    except Exception as e:
        return f"Error generating summary: {e}"