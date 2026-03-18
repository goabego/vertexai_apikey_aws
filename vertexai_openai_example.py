import openai
from google.auth import default
import google.auth.transport.requests
from google.oauth2 import service_account
 
project_id = "agent-starter-pack-spend"
location = "global"
 
# 1. Explicitly load credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file(
    "../service-account.json", 
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# 2. Force a refresh to get the actual access token string
auth_request = google.auth.transport.requests.Request()
credentials.refresh(auth_request)

 
# OpenAI Client
client = openai.OpenAI(
  base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
  api_key=credentials.token # Use the OAuth 2 access token from credentials
)
 
response = client.chat.completions.create(
  model="google/gemini-2.5-flash",
  messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain to me how AI works"}
  ]
)
 
print(response.choices[0].message)