import json
import os
import uuid

import boto3

lambda_client = boto3.client("lambda")
WORKER_FUNCTION_NAME = os.getenv("WORKER_FUNCTION_NAME")
BUCKET = os.getenv("S3_BUCKET")


def lambda_handler(event, context):
    try:
        # Parse body
        if "body" in event and isinstance(event["body"], str):
            body = json.loads(event["body"])
        else:
            body = event if isinstance(event, dict) else {}

        user_prompt = body.get("prompt", "Generate a news report on current events")
        job_id = str(uuid.uuid4())

        # Payload for the worker
        worker_payload = {"prompt": user_prompt, "job_id": job_id}

        # Invoke Worker Lambda Asynchronously
        lambda_client.invoke(
            FunctionName=WORKER_FUNCTION_NAME,
            InvocationType="Event",
            Payload=json.dumps(worker_payload),
        )

        return {
            "statusCode": 202,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "message": "Workflow started successfully",
                    "job_id": job_id,
                    "status": "processing",
                    "info": f"Check the S3 bucket {BUCKET}/output/ folder in about 5 minutes.",
                }
            ),
        }

    except Exception as e:
        print(f"Error invoking worker: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
