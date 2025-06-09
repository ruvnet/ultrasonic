# Ultrasonic Agentics - Production Deployment Guide

## Table of Contents

1. [Overview](#overview)
2. [Production Deployment Strategies](#production-deployment-strategies)
3. [Docker Containerization](#docker-containerization)
4. [Cloud Deployment](#cloud-deployment)
5. [Load Balancing and Scaling](#load-balancing-and-scaling)
6. [Security Hardening](#security-hardening)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Performance Optimization](#performance-optimization)
9. [Environment Configuration](#environment-configuration)
10. [Health Checks and Alerting](#health-checks-and-alerting)
11. [SSL/TLS Configuration](#ssltls-configuration)
12. [Backup and Disaster Recovery](#backup-and-disaster-recovery)
13. [CI/CD Pipeline](#cicd-pipeline)
14. [Maintenance and Updates](#maintenance-and-updates)

## Overview

The Ultrasonic Agentics steganography service is a FastAPI-based application that provides REST endpoints for embedding and decoding encrypted commands in audio/video files using ultrasonic frequency-shift keying (FSK) techniques.

### Key Components
- **FastAPI Server**: HTTP API with file upload/download capabilities
- **Steganography Engine**: Audio/video processing with FFmpeg
- **Encryption Service**: AES-256-GCM cryptographic operations
- **Media Processing**: Large file handling and temporary storage

## Production Deployment Strategies

### 1. Single Server Deployment (Small Scale)

```bash
# Basic production setup on single server
sudo apt update && sudo apt install -y python3-pip nginx supervisor
pip install -r requirements.txt
sudo apt install -y ffmpeg

# Create system user
sudo useradd -r -s /bin/false steganography
sudo mkdir -p /opt/steganography
sudo chown steganography:steganography /opt/steganography
```

### 2. Multi-Server Deployment (Medium Scale)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   App Server 1  │    │   App Server 2  │
│    (Nginx)      │───▶│   (FastAPI)     │    │   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                └───────┬───────────────┘
                                        ▼
                              ┌─────────────────┐
                              │  Shared Storage │
                              │    (NFS/S3)     │
                              └─────────────────┘
```

### 3. Microservices Deployment (Large Scale)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    API Gateway  │    │  Embed Service  │    │ Decode Service  │
│   (Kong/Traefik)│───▶│   (Kubernetes)  │    │  (Kubernetes)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Analysis Service│    │  Media Storage  │    │  Redis Cache    │
│  (Kubernetes)   │    │      (S3)       │    │   (Cluster)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Docker Containerization

### Dockerfile

```dockerfile
# Multi-stage build for production
FROM python:3.9-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN useradd --create-home --shell /bin/bash steganography

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/steganography/.local

# Set up application directory
WORKDIR /app
COPY . .
RUN chown -R steganography:steganography /app

# Switch to non-root user
USER steganography

# Add local Python packages to PATH
ENV PATH=/home/steganography/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "agentic_commands_stego.server.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose for Development

```yaml
version: '3.8'

services:
  steganography-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=development
      - LOG_LEVEL=debug
      - MAX_FILE_SIZE=100MB
      - TEMP_DIR=/tmp/steganography
    volumes:
      - ./logs:/app/logs
      - temp_storage:/tmp/steganography
    networks:
      - steganography-network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - steganography-api
    networks:
      - steganography-network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - steganography-network
    restart: unless-stopped

volumes:
  temp_storage:
  redis_data:

networks:
  steganography-network:
    driver: bridge
```

### Production Docker Compose

```yaml
version: '3.8'

services:
  steganography-api:
    image: your-registry/steganography-api:${TAG:-latest}
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
    environment:
      - ENV=production
      - SECRET_KEY_BASE64=${SECRET_KEY_BASE64}
      - LOG_LEVEL=info
      - MAX_FILE_SIZE=500MB
      - REDIS_URL=redis://redis:6379
    secrets:
      - encryption_key
    networks:
      - steganography-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

secrets:
  encryption_key:
    external: true

networks:
  steganography-network:
    external: true
```

## Cloud Deployment

### AWS Deployment

#### 1. ECS with Fargate

```yaml
# task-definition.json
{
  "family": "steganography-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/steganographyTaskRole",
  "containerDefinitions": [
    {
      "name": "steganography-api",
      "image": "your-account.dkr.ecr.region.amazonaws.com/steganography-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "SECRET_KEY_BASE64",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:steganography-secrets"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/steganography-api",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ]
}
```

#### 2. EKS Deployment

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: steganography-api
  labels:
    app: steganography-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: steganography-api
  template:
    metadata:
      labels:
        app: steganography-api
    spec:
      containers:
      - name: steganography-api
        image: your-account.dkr.ecr.region.amazonaws.com/steganography-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENV
          value: "production"
        - name: SECRET_KEY_BASE64
          valueFrom:
            secretKeyRef:
              name: steganography-secrets
              key: secret-key
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: temp-storage
          mountPath: /tmp/steganography
      volumes:
      - name: temp-storage
        emptyDir:
          sizeLimit: 10Gi
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
---
apiVersion: v1
kind: Service
metadata:
  name: steganography-api-service
spec:
  selector:
    app: steganography-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: steganography-api-ingress
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:region:account:certificate/cert-id
spec:
  rules:
  - host: api.steganography.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: steganography-api-service
            port:
              number: 80
```

### Google Cloud Platform (GCP)

#### Cloud Run Deployment

```yaml
# cloudrun-service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: steganography-api
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cpu-throttling: "false"
        run.googleapis.com/execution-environment: gen2
    spec:
      containerConcurrency: 10
      timeoutSeconds: 300
      containers:
      - image: gcr.io/your-project/steganography-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENV
          value: "production"
        - name: SECRET_KEY_BASE64
          valueFrom:
            secretKeyRef:
              name: steganography-secrets
              key: secret-key
        resources:
          limits:
            cpu: "2000m"
            memory: "4Gi"
        volumeMounts:
        - name: temp-storage
          mountPath: /tmp/steganography
      volumes:
      - name: temp-storage
        emptyDir:
          sizeLimit: 10Gi
```

### Azure Deployment

#### Container Instances

```yaml
# azure-container-group.yaml
apiVersion: 2019-12-01
location: East US
name: steganography-api-group
properties:
  containers:
  - name: steganography-api
    properties:
      image: your-registry.azurecr.io/steganography-api:latest
      resources:
        requests:
          cpu: 1.0
          memoryInGb: 2.0
        limits:
          cpu: 2.0
          memoryInGb: 4.0
      ports:
      - port: 8000
        protocol: TCP
      environmentVariables:
      - name: ENV
        value: production
      - name: SECRET_KEY_BASE64
        secureValue: your-secret-key-base64
      volumeMounts:
      - name: temp-storage
        mountPath: /tmp/steganography
  osType: Linux
  restartPolicy: OnFailure
  ipAddress:
    type: Public
    ports:
    - protocol: TCP
      port: 8000
    dnsNameLabel: steganography-api
  volumes:
  - name: temp-storage
    emptyDir: {}
type: Microsoft.ContainerInstance/containerGroups
```

## Load Balancing and Scaling

### Nginx Load Balancer Configuration

```nginx
# /etc/nginx/sites-available/steganography-api
upstream steganography_backend {
    least_conn;
    server 10.0.1.10:8000 max_fails=3 fail_timeout=30s;
    server 10.0.1.11:8000 max_fails=3 fail_timeout=30s;
    server 10.0.1.12:8000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    listen 443 ssl http2;
    server_name api.steganography.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/steganography.crt;
    ssl_certificate_key /etc/ssl/private/steganography.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

    # File Upload Limits
    client_max_body_size 500M;
    client_body_timeout 300s;
    client_header_timeout 60s;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        application/json
        application/javascript
        text/css
        text/javascript
        text/xml
        application/xml
        application/xml+rss;

    location / {
        proxy_pass http://steganography_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        
        # Buffering for large files
        proxy_buffering off;
        proxy_request_buffering off;
    }

    location /health {
        proxy_pass http://steganography_backend;
        proxy_connect_timeout 5s;
        proxy_send_timeout 5s;
        proxy_read_timeout 5s;
    }
}
```

### Auto-scaling Configuration

#### Kubernetes HPA

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: steganography-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: steganography-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
```

## Security Hardening

### Application Security

```python
# production_config.py
import os
from cryptography.fernet import Fernet

class ProductionConfig:
    # Environment
    ENV = "production"
    DEBUG = False
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY_BASE64')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY_BASE64 environment variable is required")
    
    # CORS - Restrict origins in production
    ALLOWED_ORIGINS = [
        "https://yourdomain.com",
        "https://app.yourdomain.com"
    ]
    
    # File Upload Security
    MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 500 * 1024 * 1024))  # 500MB
    ALLOWED_EXTENSIONS = {
        'audio': ['.mp3', '.wav', '.flac', '.ogg', '.m4a'],
        'video': ['.mp4', '.avi', '.mov', '.mkv']
    }
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', 60))
    RATE_LIMIT_PER_HOUR = int(os.environ.get('RATE_LIMIT_PER_HOUR', 1000))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Temporary File Security
    TEMP_DIR = os.environ.get('TEMP_DIR', '/tmp/steganography')
    TEMP_FILE_TTL = int(os.environ.get('TEMP_FILE_TTL', 3600))  # 1 hour
    
    @staticmethod
    def validate_file_type(filename: str, file_type: str) -> bool:
        """Validate uploaded file types."""
        allowed = ProductionConfig.ALLOWED_EXTENSIONS.get(file_type, [])
        return any(filename.lower().endswith(ext) for ext in allowed)
```

### Enhanced Security Middleware

```python
# security_middleware.py
import time
import hashlib
from fastapi import Request, HTTPException
from fastapi.middleware.base import BaseHTTPMiddleware
from collections import defaultdict, deque
import redis

class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_client=None):
        super().__init__(app)
        self.redis_client = redis_client or redis.Redis()
        self.rate_limits = defaultdict(lambda: deque())
    
    async def dispatch(self, request: Request, call_next):
        # Rate limiting
        client_ip = request.client.host
        current_time = time.time()
        
        # Check rate limit
        rate_key = f"rate_limit:{client_ip}"
        request_count = self.redis_client.incr(rate_key)
        if request_count == 1:
            self.redis_client.expire(rate_key, 60)  # 1 minute window
        
        if request_count > 60:  # 60 requests per minute
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # Content-Type validation for file uploads
        if request.method == "POST" and "multipart/form-data" in request.headers.get("content-type", ""):
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > 500 * 1024 * 1024:  # 500MB
                raise HTTPException(status_code=413, detail="File too large")
        
        # Security headers
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response
```

### Container Security

```dockerfile
# Security-hardened Dockerfile
FROM python:3.9-slim

# Update packages and install security updates
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user with specific UID/GID
RUN groupadd -r -g 1000 steganography && \
    useradd -r -g steganography -u 1000 -m -d /app steganography

# Set up application directory with proper permissions
WORKDIR /app
COPY --chown=steganography:steganography . .

# Install Python dependencies as non-root user
USER steganography
RUN pip install --user --no-cache-dir -r requirements.txt

# Remove unnecessary files
RUN find /app -name "*.pyc" -delete && \
    find /app -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Set environment variables
ENV PATH=/app/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)"

# Expose port
EXPOSE 8000

# Run with non-root user
CMD ["python", "-m", "uvicorn", "agentic_commands_stego.server.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Monitoring and Logging

### Structured Logging Configuration

```python
# logging_config.py
import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict

class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'operation'):
            log_entry['operation'] = record.operation
        if hasattr(record, 'file_size'):
            log_entry['file_size'] = record.file_size
        if hasattr(record, 'processing_time'):
            log_entry['processing_time'] = record.processing_time
        
        return json.dumps(log_entry)

def setup_logging():
    """Configure structured logging for production."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Remove default handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create structured handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())
    logger.addHandler(handler)
    
    # Set levels for specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
```

### Application Metrics

```python
# metrics.py
import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware

# Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

FILE_PROCESSING_DURATION = Histogram(
    'file_processing_duration_seconds',
    'File processing duration',
    ['operation', 'file_type']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active HTTP requests'
)

FILE_SIZE_PROCESSED = Histogram(
    'file_size_bytes',
    'Size of processed files',
    ['operation', 'file_type']
)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        ACTIVE_REQUESTS.inc()
        
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            status_code = 500
            raise
        finally:
            ACTIVE_REQUESTS.dec()
            duration = time.time() - start_time
            
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=status_code
            ).inc()
            
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
        
        return response
```

### Monitoring Stack (Prometheus + Grafana)

```yaml
# monitoring-stack.yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    networks:
      - monitoring

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
    networks:
      - monitoring

volumes:
  prometheus_data:
  grafana_data:

networks:
  monitoring:
    driver: bridge
```

## Performance Optimization

### FastAPI Optimization

```python
# optimized_api.py
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import asyncio
import aiofiles
from concurrent.futures import ThreadPoolExecutor

# Configure FastAPI for production
app = FastAPI(
    title="Agentic Commands Steganography API",
    docs_url=None,  # Disable docs in production
    redoc_url=None,  # Disable redoc in production
    openapi_url=None  # Disable OpenAPI schema
)

# Add middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["api.steganography.yourdomain.com", "localhost"]
)

# Thread pool for CPU-intensive operations
thread_pool = ThreadPoolExecutor(max_workers=4)

# Optimized file handling
async def process_file_async(file_path: str, operation: str):
    """Process file in thread pool to avoid blocking."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(thread_pool, process_file_sync, file_path, operation)

def process_file_sync(file_path: str, operation: str):
    """Synchronous file processing."""
    # Actual processing logic here
    pass

# Background task for cleanup
async def cleanup_temp_files(file_paths: list):
    """Clean up temporary files in background."""
    for file_path in file_paths:
        try:
            await aiofiles.os.remove(file_path)
        except OSError:
            pass

@app.post("/embed/audio")
async def embed_audio_optimized(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    # Process file
    result = await process_file_async(file, "embed")
    
    # Schedule cleanup
    background_tasks.add_task(cleanup_temp_files, [temp_file_path])
    
    return result
```

### Redis Caching Layer

```python
# cache.py
import redis
import json
import hashlib
from typing import Any, Optional

class CacheService:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
        self.default_ttl = 3600  # 1 hour
    
    def generate_cache_key(self, operation: str, file_hash: str, params: dict) -> str:
        """Generate cache key for operation."""
        params_str = json.dumps(params, sort_keys=True)
        key_data = f"{operation}:{file_hash}:{params_str}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get cached result."""
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Cache result."""
        try:
            ttl = ttl or self.default_ttl
            data = json.dumps(value)
            return self.redis_client.setex(key, ttl, data)
        except Exception:
            return False
    
    async def invalidate_pattern(self, pattern: str):
        """Invalidate cache entries matching pattern."""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception:
            pass
```

## Environment Configuration

### Production Environment Variables

```bash
# .env.production
# Application
ENV=production
DEBUG=false
LOG_LEVEL=info

# Security
SECRET_KEY_BASE64=your-base64-encoded-secret-key
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# File Handling
MAX_FILE_SIZE=524288000  # 500MB
TEMP_DIR=/tmp/steganography
TEMP_FILE_TTL=3600

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Database/Cache
REDIS_URL=redis://redis-cluster:6379
DATABASE_URL=postgresql://user:pass@db:5432/steganography

# Monitoring
PROMETHEUS_METRICS=true
JAEGER_ENDPOINT=http://jaeger:14268/api/traces

# External Services
AWS_REGION=us-west-2
AWS_S3_BUCKET=steganography-storage
```

### Configuration Management

```python
# config.py
import os
from typing import List
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    # Application
    env: str = "development"
    debug: bool = False
    log_level: str = "info"
    
    # Security
    secret_key_base64: str
    allowed_origins: List[str] = ["*"]
    
    # File Handling
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    temp_dir: str = "/tmp/steganography"
    temp_file_ttl: int = 3600
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    
    # External Services
    redis_url: str = "redis://localhost:6379"
    database_url: str = None
    
    # AWS
    aws_region: str = "us-west-2"
    aws_s3_bucket: str = None
    
    @validator('allowed_origins', pre=True)
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
```

## Health Checks and Alerting

### Comprehensive Health Checks

```python
# health.py
import asyncio
import time
from typing import Dict, Any
from fastapi import HTTPException
import redis
import subprocess

class HealthChecker:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.start_time = time.time()
    
    async def check_api_health(self) -> Dict[str, Any]:
        """Check API component health."""
        return {
            "status": "healthy",
            "uptime": time.time() - self.start_time,
            "timestamp": time.time()
        }
    
    async def check_redis_health(self) -> Dict[str, Any]:
        """Check Redis connectivity."""
        try:
            start = time.time()
            self.redis_client.ping()
            response_time = time.time() - start
            return {
                "status": "healthy",
                "response_time": response_time
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def check_ffmpeg_health(self) -> Dict[str, Any]:
        """Check FFmpeg availability."""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, timeout=5)
            return {
                "status": "healthy" if result.returncode == 0 else "unhealthy",
                "version": result.stdout.decode().split('\n')[0] if result.returncode == 0 else None
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def check_disk_space(self) -> Dict[str, Any]:
        """Check available disk space."""
        try:
            import shutil
            total, used, free = shutil.disk_usage("/tmp")
            free_percent = (free / total) * 100
            
            status = "healthy" if free_percent > 10 else "warning" if free_percent > 5 else "critical"
            
            return {
                "status": status,
                "free_space_gb": free // (1024**3),
                "free_percent": free_percent
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def comprehensive_health_check(self) -> Dict[str, Any]:
        """Run all health checks."""
        checks = await asyncio.gather(
            self.check_api_health(),
            self.check_redis_health(),
            self.check_ffmpeg_health(),
            self.check_disk_space(),
            return_exceptions=True
        )
        
        results = {
            "api": checks[0],
            "redis": checks[1],
            "ffmpeg": checks[2],
            "disk": checks[3]
        }
        
        # Determine overall status
        overall_status = "healthy"
        for check in results.values():
            if isinstance(check, Exception):
                overall_status = "unhealthy"
                break
            elif check.get("status") in ["unhealthy", "critical"]:
                overall_status = "unhealthy"
                break
            elif check.get("status") == "warning" and overall_status == "healthy":
                overall_status = "warning"
        
        return {
            "status": overall_status,
            "timestamp": time.time(),
            "checks": results
        }
```

### Alerting Configuration

```yaml
# alertmanager.yml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alerts@steganography.yourdomain.com'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'

receivers:
- name: 'web.hook'
  email_configs:
  - to: 'ops-team@yourdomain.com'
    subject: 'Steganography API Alert: {{ .GroupLabels.alertname }}'
    body: |
      {{ range .Alerts }}
      Alert: {{ .Annotations.summary }}
      Description: {{ .Annotations.description }}
      Instance: {{ .Labels.instance }}
      Severity: {{ .Labels.severity }}
      {{ end }}
  webhook_configs:
  - url: 'http://slack-webhook:3000/alerts'

inhibit_rules:
- source_match:
    severity: 'critical'
  target_match:
    severity: 'warning'
  equal: ['alertname', 'dev', 'instance']
```

## SSL/TLS Configuration

### Nginx SSL Configuration

```nginx
# SSL configuration for production
server {
    listen 443 ssl http2;
    server_name api.steganography.yourdomain.com;

    # SSL Certificate
    ssl_certificate /etc/ssl/certs/steganography.crt;
    ssl_certificate_key /etc/ssl/private/steganography.key;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/ssl/certs/ca-bundle.crt;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Location blocks...
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name api.steganography.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### Let's Encrypt Automation

```bash
#!/bin/bash
# ssl-renewal.sh - Automated SSL certificate renewal

DOMAIN="api.steganography.yourdomain.com"
EMAIL="admin@yourdomain.com"

# Request certificate
certbot certonly \
    --nginx \
    --email "$EMAIL" \
    --agree-tos \
    --non-interactive \
    --domains "$DOMAIN"

# Test certificate renewal
certbot renew --dry-run

# Set up automatic renewal
echo "0 2 * * * /usr/bin/certbot renew --quiet && systemctl reload nginx" | crontab -
```

## Backup and Disaster Recovery

### Backup Strategy

```bash
#!/bin/bash
# backup.sh - Comprehensive backup script

BACKUP_DIR="/opt/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup configuration files
tar -czf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" \
    /etc/nginx/sites-available/steganography-api \
    /opt/steganography/.env \
    /opt/steganography/docker-compose.yml

# Backup application logs
tar -czf "$BACKUP_DIR/logs_$TIMESTAMP.tar.gz" \
    /var/log/steganography/ \
    /var/log/nginx/steganography*

# Database backup (if applicable)
if [ -n "$DATABASE_URL" ]; then
    pg_dump "$DATABASE_URL" | gzip > "$BACKUP_DIR/database_$TIMESTAMP.sql.gz"
fi

# Redis backup
redis-cli BGSAVE
cp /var/lib/redis/dump.rdb "$BACKUP_DIR/redis_$TIMESTAMP.rdb"

# Sync to remote storage
aws s3 sync "$BACKUP_DIR" s3://steganography-backups/

# Clean up old backups
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "*.rdb" -mtime +$RETENTION_DAYS -delete

echo "Backup completed: $TIMESTAMP"
```

### Disaster Recovery Plan

```yaml
# disaster-recovery.yml
# Kubernetes disaster recovery configuration

apiVersion: v1
kind: ConfigMap
metadata:
  name: disaster-recovery-plan
data:
  recovery-steps.md: |
    # Disaster Recovery Steps
    
    ## 1. Assessment (RTO: 5 minutes)
    - Check monitoring dashboards
    - Identify scope of failure
    - Determine recovery strategy
    
    ## 2. Service Recovery (RTO: 15 minutes)
    ```bash
    # Scale up in different AZ
    kubectl scale deployment steganography-api --replicas=5
    
    # Switch traffic to backup region
    kubectl patch ingress steganography-api-ingress -p '{"spec":{"rules":[{"host":"api.steganography.yourdomain.com","http":{"paths":[{"path":"/","pathType":"Prefix","backend":{"service":{"name":"steganography-api-backup","port":{"number":80}}}}]}}]}}'
    ```
    
    ## 3. Data Recovery (RTO: 30 minutes)
    ```bash
    # Restore from latest backup
    aws s3 cp s3://steganography-backups/database_latest.sql.gz .
    gunzip database_latest.sql.gz
    psql $DATABASE_URL < database_latest.sql
    
    # Restore Redis data
    aws s3 cp s3://steganography-backups/redis_latest.rdb /var/lib/redis/dump.rdb
    systemctl restart redis
    ```
    
    ## 4. Validation (RTO: 45 minutes)
    - Run health checks
    - Test core functionality
    - Monitor error rates
    - Notify stakeholders
```

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  release:
    types: [published]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=agentic_commands_stego --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  build:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
    - name: Deploy to staging
      run: |
        # Deploy to staging environment
        kubectl set image deployment/steganography-api \
          steganography-api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          --namespace=staging
        
        # Wait for rollout
        kubectl rollout status deployment/steganography-api --namespace=staging

  integration-tests:
    needs: deploy-staging
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run integration tests
      run: |
        # Run integration tests against staging
        python -m pytest tests/integration/ --staging-url=https://staging-api.steganography.yourdomain.com

  deploy-production:
    needs: integration-tests
    runs-on: ubuntu-latest
    environment: production
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        # Blue-green deployment
        kubectl set image deployment/steganography-api-green \
          steganography-api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          --namespace=production
        
        # Wait for rollout
        kubectl rollout status deployment/steganography-api-green --namespace=production
        
        # Switch traffic
        kubectl patch service steganography-api-service \
          -p '{"spec":{"selector":{"version":"green"}}}' \
          --namespace=production
        
        # Scale down blue deployment
        kubectl scale deployment steganography-api-blue --replicas=0 --namespace=production
```

## Maintenance and Updates

### Rolling Update Strategy

```bash
#!/bin/bash
# rolling-update.sh - Zero-downtime rolling update

NEW_IMAGE="$1"
NAMESPACE="production"
DEPLOYMENT="steganography-api"

if [ -z "$NEW_IMAGE" ]; then
    echo "Usage: $0 <new-image>"
    exit 1
fi

echo "Starting rolling update to $NEW_IMAGE"

# Update deployment
kubectl set image deployment/$DEPLOYMENT \
    steganography-api=$NEW_IMAGE \
    --namespace=$NAMESPACE

# Monitor rollout
kubectl rollout status deployment/$DEPLOYMENT \
    --namespace=$NAMESPACE \
    --timeout=600s

# Verify deployment
if kubectl rollout status deployment/$DEPLOYMENT --namespace=$NAMESPACE | grep -q "successfully rolled out"; then
    echo "✅ Rolling update completed successfully"
    
    # Run health checks
    HEALTH_URL="https://api.steganography.yourdomain.com/health"
    for i in {1..5}; do
        if curl -f "$HEALTH_URL" > /dev/null 2>&1; then
            echo "✅ Health check $i/5 passed"
        else
            echo "❌ Health check $i/5 failed"
            kubectl rollout undo deployment/$DEPLOYMENT --namespace=$NAMESPACE
            exit 1
        fi
        sleep 10
    done
    
    echo "✅ All health checks passed"
else
    echo "❌ Rolling update failed"
    kubectl rollout undo deployment/$DEPLOYMENT --namespace=$NAMESPACE
    exit 1
fi
```

### Maintenance Scripts

```bash
#!/bin/bash
# maintenance.sh - Routine maintenance tasks

LOG_DIR="/var/log/steganography"
TEMP_DIR="/tmp/steganography"
RETENTION_DAYS=7

echo "Starting maintenance tasks..."

# Clean up old log files
find "$LOG_DIR" -name "*.log" -mtime +$RETENTION_DAYS -delete
echo "✅ Cleaned up old log files"

# Clean up temporary files
find "$TEMP_DIR" -type f -mtime +1 -delete
echo "✅ Cleaned up temporary files"

# Docker cleanup
docker system prune -f --volumes
echo "✅ Cleaned up Docker resources"

# Redis memory optimization
redis-cli MEMORY PURGE
echo "✅ Optimized Redis memory"

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "⚠️  Warning: Disk usage is ${DISK_USAGE}%"
    # Send alert
    curl -X POST "$SLACK_WEBHOOK_URL" \
        -H 'Content-type: application/json' \
        --data '{"text":"🚨 Steganography API: High disk usage detected ('"$DISK_USAGE"'%)"}'
fi

# Database maintenance (if applicable)
if [ -n "$DATABASE_URL" ]; then
    psql "$DATABASE_URL" -c "VACUUM ANALYZE;"
    echo "✅ Database maintenance completed"
fi

echo "Maintenance tasks completed"
```

This comprehensive deployment guide provides production-ready configurations and best practices for deploying the Ultrasonic Agentics steganography service across various environments and scales. The guide includes security hardening, monitoring, performance optimization, and operational procedures essential for maintaining a robust production service.