import boto3
import json

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('YourTableName')
    
    try:
        # Update item in DynamoDB
        response = table.update_item(
            Key={
                'id': event['id']  # Primary key
            },
            UpdateExpression='SET #n = :name, #a = :age',  # Specify attributes to update
            ExpressionAttributeNames={
                '#n': 'name',  # Using expression attribute names to handle reserved words
                '#a': 'age'
            },
            ExpressionAttributeValues={
                ':name': event['name'],
                ':age': event['age']
            },
            ReturnValues="UPDATED_NEW"  # Returns the new values of updated attributes
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Item updated successfully',
                'updatedAttributes': response['Attributes']
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error updating item',
                'error': str(e)
            })
        }
