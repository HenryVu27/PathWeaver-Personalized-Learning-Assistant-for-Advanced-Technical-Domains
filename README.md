# PathWeaver AI

An MLOps-driven personalized learning navigator for advanced technical domains, built on AWS.

## Overview

PathWeaver AI is an intelligent platform that generates personalized learning pathways for advanced technical domains. It leverages cutting-edge MLOps practices, RAG (Retrieval-Augmented Generation), and LLMs on AWS to transform scattered educational resources into structured, actionable learning journeys.

## Features

- Automated resource curation and ingestion
- Intelligent knowledge graph and vector store construction
- Personalized user profiling
- Dynamic learning path generation
- Interactive path refinement and progress tracking
- Continuous learning and system improvement

## Technical Architecture

- **Frontend**: Streamlit UI
- **Backend**: AWS Lambda, API Gateway
- **Database**: Amazon OpenSearch (Vector Store), DynamoDB (User Profiles)
- **ML Infrastructure**: Amazon Bedrock, SageMaker
- **Storage**: Amazon S3
- **MLOps**: AWS CodePipeline, CloudWatch, SageMaker Pipelines

## Project Structure

```
.
├── app/                    # Streamlit frontend application
├── backend/               # AWS Lambda functions and API handlers
├── infrastructure/        # AWS CDK/CloudFormation templates
├── ml/                    # Machine learning components
│   ├── embeddings/       # Text embedding generation
│   ├── knowledge_graph/  # Knowledge graph construction
│   └── rag/             # RAG implementation
├── scripts/              # Utility scripts
├── tests/               # Test suite
└── requirements/        # Python dependencies
```

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements/dev.txt
```

2. Configure AWS credentials:
```bash
aws configure
```

3. Deploy infrastructure:
```bash
cd infrastructure
cdk deploy
```

4. Run the local development server:
```bash
cd app
streamlit run main.py
```

## Development Status

Currently in Phase 1 (MVP) development, focusing on:
- Basic path generation functionality
- RAG implementation with Amazon Bedrock
- Simple Streamlit UI
- Core AWS infrastructure setup

## License

See [LICENSE](LICENSE) for details.