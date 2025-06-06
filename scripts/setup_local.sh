#!/bin/bash

# Create and activate virtual environment
echo "Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements/dev.txt

# Set up AWS credentials if not already configured
if [ ! -f ~/.aws/credentials ]; then
    echo "AWS credentials not found. Please configure:"
    aws configure
fi

# Install AWS CDK globally
echo "Installing AWS CDK..."
npm install -g aws-cdk

# Create necessary directories if they don't exist
mkdir -p app/static
mkdir -p backend/lambda/path_generator
mkdir -p infrastructure/stacks
mkdir -p tests

# Make script executable
chmod +x scripts/setup_local.sh

echo "Setup complete! You can now:"
echo "1. Deploy infrastructure: cd infrastructure && cdk deploy"
echo "2. Run the frontend: cd app && streamlit run main.py" 