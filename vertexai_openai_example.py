import openai
import google.auth.transport.requests
from google.oauth2 import service_account

# --- CONFIGURATION ---
# project_id: The GCP Project ID where the Vertex AI API is enabled.
# location: 'global' works for the OpenAI-compatible endpoint, but specific regions 
# (e.g., 'us-central1') may be required depending on your VPC/Endpoint setup.
project_id = "UPDATE_HERE"
location = "UPDATE_HERE"

# --- DEPLOYMENT NOTES FOR AWS EC2 & SECRETS MANAGER ---
"""
INSTRUCTIONS FOR THE NEXT ENGINEER:
1. STORAGE: Do NOT store 'service-account.json' on the EC2 disk in production.
   - Upload the JSON content to AWS Secrets Manager as a 'Plaintext' secret.
   - Use 'boto3' to fetch the secret string and pass it to:
     service_account.Credentials.from_service_account_info(json.loads(secret_string))

2. PERMISSIONS (IAM): 
   - Ensure the EC2 Instance Profile has 'secretsmanager:GetSecretValue' permissions.
   - In GCP, the Service Account needs the 'Vertex AI User' role.

3. REFRESH LOGIC:
   - Google Access Tokens expire every 3600 seconds (1 hour).
   - If this script is converted to a long-running service (FastAPI/worker),
     you must call 'credentials.refresh(auth_request)' inside your request loop
     to avoid 401 Unauthorized errors after the first hour.
"""

# 1. Explicitly load credentials from the JSON file.
# The 'cloud-platform' scope is required to generate the OAuth2 token for Vertex AI.
credentials = service_account.Credentials.from_service_account_file(
    "../service-account.json", 
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# 2. Force a refresh to get the actual access token string.
# By default, loading the file doesn't "fetch" the token; .refresh() 
# performs the network call to Google's Auth server to populate credentials.token.
auth_request = google.auth.transport.requests.Request()
credentials.refresh(auth_request)

# 3. Initialize OpenAI Client using Vertex AI Endpoint.
# We point the base_url to Google's OpenAI-compatible translation layer.
# The 'api_key' here is actually the Google OAuth2 Access Token.
client = openai.OpenAI(
    base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
    api_key=credentials.token 
)

# 4. Standard OpenAI-style Completion call.
# Model mapping: 'google/gemini-2.5-flash' follows the [provider]/[model] convention.
try:
    response = client.chat.completions.create(
        model="google/gemini-2.5-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain to me how AI works"}
        ]
    )
    print(response.choices[0].message.content)

except Exception as e:
    print(f"Error calling Vertex AI via OpenAI SDK: {e}")
    # Logic for token expiration recovery could be added here.