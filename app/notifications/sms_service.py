def send_sms_notification(

    alert
):

    transaction = alert[
        "transaction"
    ]

    print(
        "\nSIMULATED SMS SENT\n"
    )

    print(
        f"""
ALERT TYPE:
{alert.get('alert_type', [])}

MESSAGE:
{alert.get('alert_message')}

TRANSACTION DETAILS:

Date:
{transaction['transaction_date']}

Description:
{transaction['description']}

Amount:
{transaction['amount']} {transaction['currency']}

Transaction Type:
{transaction['transaction_type']}
"""
    )

    return {

        "delivery_status": "SENT",

        "provider": "SIMULATED_SMS"
    }