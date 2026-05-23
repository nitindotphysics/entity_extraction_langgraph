import os
import json

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def extract_bank_statement_entities(
    document_representation
):

    prompt = f"""
You are a financial entity extraction system.

Extract ONLY the following entities from this bank statement:

1. customer_name
2. customer_id
3. account_number
4. swift_code
5. opening_balance
6. closing_balance
7. transactions

For transactions extract:
- transaction_date
- description
- transaction_type (CREDIT or DEBIT)
- amount

Return ONLY valid JSON.

Required format:

{{
  "customer_entities": {{
      "customer_name": "",
      "customer_id": ""
  }},

  "account_entities": {{
      "account_number": "",
      "swift_code": ""
  }},

  "balance_entities": {{
      "opening_balance": "",
      "closing_balance": ""
  }},

  "transaction_entities": [
      {{
          "transaction_date": "",
          "description": "",
          "transaction_type": "",
          "amount": ""
      }}
  ]
}}

DOCUMENT TEXT:
-------------------
{
document_representation["content_representation"]["markdown"][:8000]
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

    print("\nRAW EXTRACTION RESPONSE:\n")
    print(content)

    # REMOVE MARKDOWN WRAPPERS

    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    try:
        entities = json.loads(content)

    except json.JSONDecodeError:

        entities = {
            "error": "Failed to parse extraction JSON",
            "raw_response": content
        }

    return entities