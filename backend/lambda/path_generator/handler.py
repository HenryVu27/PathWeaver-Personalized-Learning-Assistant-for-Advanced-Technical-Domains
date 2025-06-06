import json
import os
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from botocore.exceptions import ClientError
from typing import Dict, Any

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
bedrock = boto3.client('bedrock-runtime')

# Initialize OpenSearch client
OPENSEARCH_DOMAIN = os.environ['OPENSEARCH_DOMAIN']
opensearch_client = OpenSearch(
    hosts=[{'host': OPENSEARCH_DOMAIN, 'port': 443}],
    http_auth=None,  # We're using IAM role-based auth
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def get_user_profile(user_id: str) -> Dict[str, Any]:
    """Retrieve user profile from DynamoDB."""
    table = dynamodb.Table(os.environ['USER_TABLE'])
    try:
        response = table.get_item(Key={'user_id': user_id})
        return response.get('Item', {})
    except ClientError as e:
        print(f"Error getting user profile: {e}")
        return {}

def query_vector_store(query: str, user_profile: Dict[str, Any]) -> list:
    """Query OpenSearch for relevant learning resources."""
    try:
        # Here we would normally generate embeddings for the query
        # For MVP, we'll use basic keyword search
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["content", "title", "description"]
                }
            }
        }
        
        response = opensearch_client.search(
            index="learning_resources",
            body=search_body,
            size=5
        )
        
        return [hit['_source'] for hit in response['hits']['hits']]
    except Exception as e:
        print(f"Error querying vector store: {e}")
        return []

def generate_learning_path(query: str, relevant_resources: list, user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Generate personalized learning path using Bedrock."""
    try:
        # Construct prompt for the LLM
        prompt = f"""Given the user's query: "{query}"
And their profile:
{json.dumps(user_profile, indent=2)}

Using these relevant resources:
{json.dumps(relevant_resources, indent=2)}

Generate a structured learning path that includes:
1. Prerequisites
2. Learning steps in sequence
3. Estimated time for each step
4. Specific resources to use for each step

Format the response as JSON with the following structure:
{{
    "prerequisites": [list of prerequisites],
    "steps": [
        {{
            "title": "step title",
            "description": "step description",
            "estimated_time": "time in hours",
            "resources": [list of resource objects]
        }}
    ]
}}"""

        # Call Bedrock (Claude)
        response = bedrock.invoke_model(
            modelId='anthropic.claude-v2',
            body=json.dumps({
                "prompt": prompt,
                "max_tokens": 2000,
                "temperature": 0.7
            })
        )
        
        response_body = json.loads(response['body'].read())
        learning_path = json.loads(response_body['completion'])
        
        return learning_path
    except Exception as e:
        print(f"Error generating learning path: {e}")
        return {
            "error": "Failed to generate learning path",
            "details": str(e)
        }

def lambda_handler(event, context):
    """Main Lambda handler function."""
    try:
        # Parse request body
        body = json.loads(event['body'])
        query = body['query']
        user_id = body.get('user_id')
        
        # Get user profile
        user_profile = get_user_profile(user_id) if user_id else {}
        
        # Query vector store for relevant resources
        relevant_resources = query_vector_store(query, user_profile)
        
        # Generate learning path
        learning_path = generate_learning_path(query, relevant_resources, user_profile)
        
        return {
            'statusCode': 200,
            'body': json.dumps(learning_path),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error',
                'details': str(e)
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        } 