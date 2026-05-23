
from app.alerts.rule_loader import (
    load_alert_rules
)


def evaluate_alert_rules(
    normalized_entities
):

    rules = load_alert_rules()

    alerts = []

    transactions = normalized_entities[
        "transaction_entities"
    ]

    for transaction in transactions:

        for rule_name, rule in rules.items():

            # rule 1:
            # transaction type match

            if (
                "transaction_type" in rule
            ):

                if (

                    transaction[
                        "transaction_type"
                    ]

                    !=

                    rule[
                        "transaction_type"
                    ]
                ):

                    continue

            # rule 2:
            # minimum amount check

            if (
                transaction["amount"]

                <

                rule["min_amount"]
            ):

                continue

            # rule 3:
            # keyword check

            if "keyword" in rule:

                if (

                    rule["keyword"].lower()

                    not in

                    transaction[
                        "description"
                    ].lower()
                ):

                    continue

            alerts.append({

                "rule_name": rule_name,

                "alert_message":

                    rule[
                        "alert_message"
                    ],

                "transaction":

                    transaction
            })

    return alerts