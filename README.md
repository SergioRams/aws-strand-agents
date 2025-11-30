# Strands Agents, Serverless AWS News Report Workflow

Build a serverless Agentic System featuring the Strands Agents SDK. Tested on us-east-1.

pre-requisites:

    * AWS Account.
    * SAM CLI installed and configured.
    * Get Anthropic model access on Bedrock.
    * Get a Tavily API key. (free)

**Overview:**

This agentic workflow leverages the Strands Agents SDK to generate a video from a prompt.
Meant as a **"Breaking News"** project, it will search the web on the given topic, and generate a video in the style
of a news reporter hosting a breaking news story.

## Agents:
* **Director Agent:**
  * Orchestrates the workflow and output files.
* **Research Agent:**
  * uses Tavily as a tool to search the web and writes a report(s).
* **Radio Agent:**
  * Generates an audio clip from the report using Polly's voice_id corresponding to the language(s) requested while
  citing the sources in a Radio Station style.
* **Editor Agent:**
  * Picks the proper background audio and video based on the sentiment of the news report to generate the final video.


## Architecture diagram
![Alt Text](aws_serverless_agentic.png)


## Build and Deploy

```bash
# Set Docker host (if using Docker Desktop)
export DOCKER_HOST="unix://$HOME/.docker/desktop/docker.sock"

# Build
sam build

# Deploy (use --guided first time to set up ECR repository)
sam deploy --guided
```

From the root of the project run CLI commands replacing with SAM DataBucket output accordingly:
DataBucket -> Value
```
aws s3 sync background_audio/ s3://<bucket-name>/audio/
aws s3 sync video/ s3://<bucket-name>/video/
```

## How to use

Sample request:
```
curl -Method POST "<RagApiUrl>" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{
    "prompt": "Create a breaking news report on: The citrus fruits situation across the USA 2025, make it english and spanish!"
  }'
```

Sample response:

```
{
    "message": "Workflow started successfully",
    "job_id": "6362e9d2-32ce-4573-8bc6-61f7a8f86d8b",
    "status": "processing",
    "info": "Check the S3 bucket <BUCKET-NAME>/output/ folder in about 5 minutes."
}
```

Bucket outputs:
```
* output/<language><sentiment><topic>.mp4: VIDEO.
* output/<language><topic>.mp3: raw AUDIO file.
* output/news-<topic>.txt: research REPORT with sources.
* output/script-<topic>.txt: SCRIPT to be used for the audio.
```
