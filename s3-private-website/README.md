# S3 Private Website with AWS Amplify

This project demonstrates how to create a private S3 website using AWS Amplify with API Gateway integration for file uploads.

## Features
- Private S3 website hosting using AWS Amplify
- User authentication
- File upload functionality using pre-signed URLs from API Gateway
- Integration with existing API Gateway endpoint

## Prerequisites
- Node.js and npm installed
- AWS account
- AWS Amplify CLI installed (`npm install -g @aws-amplify/cli`)
- Existing API Gateway endpoint for pre-signed URL generation

## Setup Instructions
1. Initialize the project:
```bash
npm create react-app s3-private-website
cd s3-private-website
```

2. Install dependencies:
```bash
npm install @aws-amplify/ui-react aws-amplify @aws-amplify/core
```

3. Initialize Amplify:
```bash
amplify init
amplify add auth
amplify push
```

4. Update the configuration with your API Gateway endpoint
5. Deploy the application using Amplify Console

## Architecture
The application uses the following AWS services:
- AWS Amplify for hosting and authentication
- Amazon S3 for file storage
- Amazon API Gateway for pre-signed URL generation
- Amazon Cognito for user authentication