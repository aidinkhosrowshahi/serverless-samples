# File Upload Frontend Application

This frontend application uses AWS Amplify to enable file uploads to S3 via presigned URLs from API Gateway and Lambda.

## Setup Instructions

1. Install dependencies:
```bash
npm install aws-amplify @aws-amplify/ui-react
```

2. Configure Amplify:
- Update the `src/aws-exports.js` file with your API Gateway endpoint
- Configure authentication if required

3. Run the application:
```bash
npm start
```