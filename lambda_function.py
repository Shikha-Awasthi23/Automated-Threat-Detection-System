API Gateway POST request testimport json
import os
import boto3
from datetime import datetime, timezone

sns = boto3.client("sns")

SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "")


def lambda_handler(event, context):
    try:
        detail = event.get("detail", {})

        finding_type = detail.get("type", "Unknown")
        finding_id = detail.get("id", "Unknown")
        severity = detail.get("severity", "Unknown")
        title = detail.get("title", finding_type)

        account_id = event.get("account", "Unknown")
        region = event.get("region", "us-east-1")
        event_time = event.get(
            "time",
            datetime.now(timezone.utc).isoformat()
        )

        print("Received event:", json.dumps(event))

        if not SNS_TOPIC_ARN:
            raise ValueError(
                "SNS_TOPIC_ARN environment variable is missing"
            )

        message = (
            "AWS GUARD DUTY SECURITY ALERT\n\n"
            f"Finding Title: {title}\n"
            f"Finding Type: {finding_type}\n"
            f"Severity: {severity}\n"
            f"Finding ID: {finding_id}\n"
            f"AWS Account: {account_id}\n"
            f"Region: {region}\n"
            f"Event Time: {event_time}\n"
        )

        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="AWS GuardDuty Security Alert",
            Message=message
        )

        message_id = response.get("MessageId", "Unknown")

        print("SNS notification sent. Message ID:", message_id)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Security alert notification sent",
                "finding_id": finding_id,
                "sns_message_id": message_id
            })
        }

    except Exception as error:
        print("Error:", str(error))
        raise