# Case Management API for Amazon Q Custom Plugins

This project implements a serverless Case Management API using AWS Lambda and DynamoDB.

The Case Management API provides a robust solution for creating, retrieving, and listing cases. It is designed to be used as a custom plugin for Amazon Q, offering seamless integration and efficient case management capabilities.

The API is built using AWS Serverless Application Model (SAM) and leverages AWS Lambda for serverless compute and Amazon DynamoDB for persistent storage. This architecture ensures high scalability, low latency, and cost-effectiveness for managing cases in various scenarios.

## Repository Structure

```
.
└── case-management-api
    ├── README.md
    ├── src
    │   ├── amazon-q-plugins-api.yml
    │   └── api
    │       ├── __init__.py
    │       └── cases.py
    └── template.yaml
```

### Key Files:

- `case-management-api/src/api/cases.py`: Contains the main logic for case management operations.
- `case-management-api/template.yaml`: AWS SAM template defining the serverless infrastructure.
- `case-management-api/src/amazon-q-plugins-api.yml`: OpenAPI specification for the Case Management API.

## Usage Instructions

### Installation

Prerequisites:
- Python 3.9
- AWS CLI configured with appropriate permissions
- AWS SAM CLI

Steps:
1. Clone the repository:
   ```
   git clone <repository-url>
   cd case-management-api
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Deploy the application:
   ```
   sam build
   sam deploy --guided
   ```

   Follow the prompts to configure your deployment.

### API Endpoints

1. Create a new case:
   - Method: POST
   - Path: /cases
   - Body:
     ```json
     {
       "description": "Case description",
       "metadata": {
         "key1": "value1",
         "key2": "value2"
       }
     }
     ```
   - Response:
     ```json
     {
       "caseId": "uuid",
       "description": "Case description",
       "metadata": {
         "key1": "value1",
         "key2": "value2"
       },
       "createdAt": "ISO8601 timestamp",
       "updatedAt": "ISO8601 timestamp"
     }
     ```

2. Retrieve a case:
   - Method: GET
   - Path: /cases/{caseId}
   - Response:
     ```json
     {
       "caseId": "uuid",
       "description": "Case description",
       "metadata": {
         "key1": "value1",
         "key2": "value2"
       },
       "createdAt": "ISO8601 timestamp",
       "updatedAt": "ISO8601 timestamp"
     }
     ```

3. List all cases:
   - Method: GET
   - Path: /cases
   - Response:
     ```json
     {
       "cases": [
         {
           "caseId": "uuid",
           "description": "Case description",
           "metadata": {
             "key1": "value1",
             "key2": "value2"
           },
           "createdAt": "ISO8601 timestamp",
           "updatedAt": "ISO8601 timestamp"
         },
         ...
       ]
     }
     ```

4. Generate pre-signed URL for uploading case files:
   - Method: GET
   - Path: /cases/{caseId}/upload
   - Response: Pre-signed URL for file upload

### Configuration

The API uses the following environment variables:

- `CASES_TABLE`: The name of the DynamoDB table for storing cases. This is automatically set during deployment.
- `UPLOAD_BUCKET_NAME`: The name of the S3 bucket for storing case files. This is automatically set during deployment.

### Testing & Quality

To run tests:

```
python -m unittest discover tests
```

### Troubleshooting

1. Issue: API returns 500 Internal Server Error
   - Description: The API is returning unexpected 500 errors.
   - Error message: "Internal server error"
   - Diagnostic process:
     1. Check CloudWatch Logs for the Lambda function.
     2. Enable debug logging by setting the `LOG_LEVEL` environment variable to `DEBUG`.
     3. Redeploy the stack with updated logging.
   - Debug mode:
     ```
     sam deploy --parameter-overrides ParameterKey=LogLevel,ParameterValue=DEBUG
     ```
   - Expected outcome: Detailed error messages in CloudWatch Logs.

2. Issue: DynamoDB access denied
   - Description: Lambda function unable to access DynamoDB table.
   - Error message: "AccessDeniedException: User: arn:aws:sts::... is not authorized to perform: dynamodb:PutItem on resource: ..."
   - Diagnostic process:
     1. Verify IAM role permissions for the Lambda function.
     2. Check if the DynamoDB table name matches the `CASES_TABLE` environment variable.
   - Debug command:
     ```
     aws iam get-role --role-name <Lambda-Role-Name>
     ```
   - Expected outcome: IAM role should have appropriate DynamoDB permissions.

### Performance Optimization

- Monitor Lambda execution time and memory usage in CloudWatch Metrics.
- Use AWS X-Ray for tracing and identifying bottlenecks.
- Optimize DynamoDB read/write capacity units based on usage patterns.

## Data Flow

The Case Management API handles data flow through the following steps:

1. Client sends HTTP request to API Gateway endpoint.
2. API Gateway routes the request to the appropriate Lambda function.
3. Lambda function processes the request:
   - For POST requests, it creates a new case in DynamoDB.
   - For GET requests, it retrieves case(s) from DynamoDB.
4. Lambda function returns the response to API Gateway.
5. API Gateway sends the HTTP response back to the client.

```
Client <-> API Gateway <-> Lambda Function <-> DynamoDB
```

Note: Ensure proper error handling and input validation at each step to maintain data integrity and security.

## Infrastructure

The infrastructure for this project is defined in the `template.yaml` file using AWS SAM. Key resources include:

### Lambda

- `CaseManagementFunction`:
  - Handler: `api/cases.lambda_handler`
  - Runtime: Python 3.9
  - Environment Variables:
    - `CASES_TABLE`: References the DynamoDB table
    - `UPLOAD_BUCKET_NAME`: References the S3 bucket for case files
  - API Gateway Events:
    - POST /cases
    - GET /cases/{caseId}
    - GET /cases
    - GET /cases/{caseId}/upload

### DynamoDB

- `CasesTable`:
  - Partition Key: `caseId` (String)
  - Billing Mode: PAY_PER_REQUEST

### S3

- `CaseFilesBucket`:
  - CORS Configuration: Allows PUT, GET, and HEAD methods
  - Lifecycle Policy: Expires objects after 90 days
  - Public Access: Blocked

### API Gateway

- Automatically created by SAM to expose Lambda function endpoints
- Stage name configurable via `Stage` parameter

The infrastructure is designed to be scalable and cost-effective, leveraging serverless technologies for optimal performance and resource utilization.