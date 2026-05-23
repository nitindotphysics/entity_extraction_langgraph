import yaml


def load_alert_rules():

    with open(

        "config/alert_rules.yaml",

        "r"

    ) as file:

        rules = yaml.safe_load(
            file
        )

    return rules