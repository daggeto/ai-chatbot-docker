# Deployment Guide

## Local Development
Use Docker Compose for local development:
```bash
docker-compose up --build
```

## Cloud Deployment Options

### Render
1. Connect your GitHub repository
2. Set environment variables for model configuration
3. Use Docker deployment option
4. Ensure sufficient memory allocation (4GB+ recommended)

### Fly.io
1. Install flyctl CLI
2. Run `fly launch` in project directory
3. Configure fly.toml for memory requirements
4. Deploy with `fly deploy`

### AWS Fargate
1. Build and push image to ECR
2. Create ECS task definition with sufficient memory
3. Configure load balancer and security groups
4. Deploy using ECS service

## Environment Variables
- `MODEL_PATH`: Path to the GGUF model file
- `DOCS_PATH`: Path to documentation directory
- `CHROMA_PERSIST_DIR`: ChromaDB persistence directory
- `MAX_TOKENS`: Maximum tokens for LLM generation
- `TEMPERATURE`: LLM temperature setting (0.0-1.0)

## Resource Requirements
- Memory: 4GB minimum, 8GB recommended
- CPU: 2 cores minimum
- Storage: 10GB for model and vector store
