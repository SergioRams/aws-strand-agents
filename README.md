# AWS Serverless Agentic Workflow
Strands Agents


## Architecture diagram
![Alt Text](aws_serverless_agentic.png)

Upload audio to s3
```
aws s3 sync background_audio/ s3://dev-strands-agentic-data-store/audio/
aws s3 sync video/ s3://dev-strands-agentic-data-store/video/
```
