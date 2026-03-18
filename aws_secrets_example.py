import json
import boto3  # AWS SDK
import openai
import google.auth.transport.requests
from google.oauth2 import service_account
from botocore.exceptions import ClientError

# --- AWS CONFIGURATION ---
# 1. Create a Secret in AWS Secrets Manager (Type: Other/Plaintext).
# 2. Paste the entire content of your service-account.json into the secret.
# 3. Attach an IAM Role to your EC2 instance with 'secretsmanager:GetSecretValue' permissions.
# Documentation: https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_python.html
# -------------------------

def get_google_credentials_from_aws(secret_name, region_name="us-east-1"):
    """Retrieves the Google Service Account JSON from AWS Secrets Manager."""
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    # The secret string is the JSON content of your service account key
    secret_data = json.loads(get_secret_value_response['SecretString'])
    
    return service_account.Credentials.from_service_account_info(
        secret_data, 
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

project_id = "UPDATE_HERE"
location = "UPDATE_HERE"

# Step 1: Fetch credentials from AWS instead of a local file
# Replace 'my-google-sa-secret' with your actual AWS Secret name
credentials = get_google_credentials_from_aws("my-google-sa-secret")

# Step 2: Refresh the token (The "1-hour" pass)
auth_request = google.auth.transport.requests.Request()
credentials.refresh(auth_request)

# Step 3: Initialize OpenAI Client
client = openai.OpenAI(
  base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
  api_key=credentials.token 
)

# Step 4: Execute Call
response = client.chat.completions.create(
  model="google/gemini-2.5-flash",
  messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain to me how AI works"}
  ]
)

print(response.choices[0].message.content)