from dateutil import parser

from app.models.transaction_models import (
    BankStatementEntities
)


def clean_amount(amount_str):

    amount_str = (
        amount_str
        .replace("$", "")
        .replace(",", "")
        .strip()
    )

    return float(amount_str)


def normalize_transaction(transaction):

    normalized_transaction = {

        "transaction_date": parser.parse(
            transaction["transaction_date"]
        ).date(),

        "description": transaction["description"],

        "transaction_type": transaction[
            "transaction_type"
        ].upper(),

        "amount": clean_amount(
            transaction["amount"]
        ),

        "currency": "USD"
    }

    return normalized_transaction


def normalize_bank_statement_entities(
    extracted_entities
):

    normalized_transactions = []

    for transaction in extracted_entities[
        "transaction_entities"
    ]:

        normalized_transactions.append(
            normalize_transaction(transaction)
        )

    normalized_data = {

        "customer_entities": {
            "customer_name": extracted_entities[
                "customer_entities"
            ]["customer_name"],

            "customer_id": extracted_entities[
                "customer_entities"
            ]["customer_id"].replace("-", "")
        },

        "account_entities": extracted_entities[
            "account_entities"
        ],

        "balance_entities": {

            "opening_balance": clean_amount(
                extracted_entities[
                    "balance_entities"
                ]["opening_balance"]
            ),

            "closing_balance": clean_amount(
                extracted_entities[
                    "balance_entities"
                ]["closing_balance"]
            ),

            "currency": "USD"
        },

        "transaction_entities": (
            normalized_transactions
        )
    }

    validated_entities = (
        BankStatementEntities(
            **normalized_data
        )
    )

    return validated_entities