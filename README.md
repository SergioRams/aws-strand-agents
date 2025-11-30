# AWS Serverless Agentic Workflow
Strands Agents


## Architecture diagram
![Alt Text](aws_serverless_agentic.png)

Upload audio to s3
```
aws s3 sync background_audio/ s3://dev-strands-agentic-data-store/audio/
aws s3 sync video/ s3://dev-strands-agentic-data-store/video/
```

```
{
    "prompt": "Need to create a breaking news project on: Citrus fruits situation across the USA 2025, make it spanish and english"
}
```


## Build and Deploy

```bash
# Set Docker host (if using Docker Desktop)
export DOCKER_HOST="unix://$HOME/.docker/desktop/docker.sock"

# Build (creates ECR repo automatically on first deploy)
sam build

# Deploy (use --guided first time to set up ECR repository)
sam deploy --guided
```

## Clean up old Docker images

```bash
# Remove dangling images
docker image prune -f
```
