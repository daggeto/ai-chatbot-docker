# AWS Fargate Deployment Guide

## Prerequisites
- AWS CLI configured
- Docker installed
- AWS Copilot CLI (optional, recommended)

## Using AWS Copilot (Recommended)

1. **Initialize Copilot application:**
   ```bash
   copilot app init ai-chatbot
   cd ai-chatbot
   ```

2. **Create environment:**
   ```bash
   copilot env init --name production
   copilot env deploy --name production
   ```

3. **Create service:**
   ```bash
   copilot svc init --name api --svc-type "Backend Service"
   ```

4. **Configure copilot/api/copilot.yml:**
   ```yaml
   name: api
   type: Backend Service
   
   http:
     healthcheck: '/health'
   
   image:
     build: './backend/Dockerfile'
   
   secrets:
     - MODEL_PATH
     - DOCS_PATH
   
   variables:
     CHROMA_PERSIST_DIR: /app/chroma_db
     MAX_TOKENS: 512
     TEMPERATURE: 0.7
   
   count:
     min: 1
     max: 3
     cooldown:
       scale_in_cooldown: 300s
       scale_out_cooldown: 120s
   
   network:
     vpc:
       enable_logs: true
   
   storage:
     volumes:
       chroma_data:
         path: /app/chroma_db
         read_only: false
   
   exec: true
   logging: true
   ```

5. **Deploy service:**
   ```bash
   copilot svc deploy --name api --env production
   ```

## Manual ECS Deployment

1. **Build and push to ECR:**
   ```bash
   aws ecr create-repository --repository-name ai-chatbot-api
   docker build -t ai-chatbot-api ./backend
   docker tag ai-chatbot-api:latest <account-id>.dkr.ecr.<region>.amazonaws.com/ai-chatbot-api:latest
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ai-chatbot-api:latest
   ```

2. **Create ECS task definition:**
   ```json
   {
     "family": "ai-chatbot-api",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "2048",
     "memory": "4096",
     "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "ai-chatbot-api",
         "image": "<account-id>.dkr.ecr.<region>.amazonaws.com/ai-chatbot-api:latest",
         "portMappings": [
           {
             "containerPort": 8000,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {"name": "MODEL_PATH", "value": "/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"},
           {"name": "DOCS_PATH", "value": "/app/docs"},
           {"name": "CHROMA_PERSIST_DIR", "value": "/app/chroma_db"}
         ],
         "healthCheck": {
           "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
           "interval": 30,
           "timeout": 5,
           "retries": 3
         },
         "logConfiguration": {
           "logDriver": "awslogs",
           "options": {
             "awslogs-group": "/ecs/ai-chatbot-api",
             "awslogs-region": "<region>",
             "awslogs-stream-prefix": "ecs"
           }
         }
       }
     ]
   }
   ```

3. **Create ECS service and configure load balancer as needed**

## Resource Requirements
- **CPU**: 2 vCPUs minimum
- **Memory**: 4GB minimum (8GB recommended)
- **Storage**: 10GB for models and vector store
- **Network**: VPC with internet gateway for model downloads
