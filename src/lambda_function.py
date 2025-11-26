import json
import os

from director_agent import director_agent


def lambda_handler(event, context):
    """
    AWS Lambda entry point for Strand Agents workflow
    """
    try:
        # Extract user query from event
        user_prompt = event.get("prompt", "Generate a news report on current events")

        # Call the director agent with the user query
        response = director_agent(user_prompt)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Workflow completed successfully",
                    "response": str(response),
                    "s3_bucket": os.getenv("S3_BUCKET"),
                }
            ),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e), "message": "Workflow failed"}),
        }
