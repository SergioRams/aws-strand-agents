import os

from director_agent import director_agent


def lambda_handler(event, context):
    """
    Background Worker for Strand Agents.
    Triggered asynchronously by API Handler.
    Event comes from api_handler.py: {"prompt": "...", "job_id": "..."}
    """
    user_prompt = event.get("prompt", "Generate a news report on current events")
    job_id = event.get("job_id", "unknown-job")
    s3_bucket = os.getenv("S3_BUCKET")

    print(f"Starting Background Job {job_id} with prompt: {user_prompt}")

    try:
        # Call the director agent (This takes minutes)
        response = director_agent(user_prompt)

        print(f"Job {job_id} Completed Successfully.")
        print(f"Agent Response: {response}")

        return {"status": "success", "job_id": job_id, "bucket": s3_bucket}

    except Exception as e:
        print(f"Job {job_id} FAILED: {str(e)}")
        raise e
