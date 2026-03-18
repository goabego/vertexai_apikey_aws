# Vertex AI OpenAI-Compatible Endpoint Examples

This directory contains examples of how to interact with Google Vertex AI models (like Gemini) using the standard OpenAI Python SDK.

## Files

### 1. `vertexai_openai_example.py`
A standalone script demonstrating how to:
- Load a Google Service Account JSON file.
- Generate an OAuth2 access token.
- Configure the `openai` client to point to the Vertex AI base URL.
- Make a chat completion call using the `google/gemini-2.5-flash` model.

### 2. `aws_secrets_example.py`
A production-ready pattern for AWS environments (EC2/Lambda):
- Uses `boto3` to retrieve the Google Service Account credentials from **AWS Secrets Manager**.
- Eliminates the need to store sensitive `.json` files on the local disk.
- Demonstrates the token refresh logic required for long-running processes.

## Setup Requirements

1. **GCP Side**:
   - Enable the Vertex AI API.
   - Create a Service Account with the `Vertex AI User` role.
   - Download the JSON key.

2. **AWS Side (for `aws_secrets_example.py`)**:
   - Store the JSON key content in Secrets Manager.
   - Ensure the execution environment has `secretsmanager:GetSecretValue` IAM permissions.

3. **Python Environment**:
   ```bash
   pip install openai boto3 google-auth
   ```

## Usage
Update the `project_id` and `location` variables in either script and run:
```bash
python vertexai_openai_example.py
```