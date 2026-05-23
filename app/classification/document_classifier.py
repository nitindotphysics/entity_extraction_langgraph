import os
import json

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def classify_document(document_representation):

    prompt = f"""
You are a financial document classifier.

Analyze the following financial document text.

Classify it into ONE category:

- bank_statement
- invoice
- aml_report
- loan_document
- reconciliation_report
- unknown

Return ONLY valid JSON.

Do NOT include:
- markdown
- explanation
- ```json
- extra text

Required JSON format:

{{
    "document_type": "string",
    "confidence": float,
    "reasoning": [
        "reason 1",
        "reason 2"
    ]
}}

DOCUMENT TEXT:
-------------------
{
document_representation["content_representation"]["markdown"][:4000]
}

"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    print("\nRAW LLM RESPONSE:\n")
    print(content)

    try:
        classification = json.loads(content)

    except json.JSONDecodeError:

        print("\nJSON PARSING FAILED\n")

        classification = {
            "document_type": "unknown",
            "confidence": 0.0,
            "reasoning": [
                "Failed to parse LLM JSON output"
            ]
        }

    return classification