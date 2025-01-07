import boto3
from datetime import datetime

class CustomerPurchaseProcessor:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('customer_purchases')
    
    def process_purchase(self, customer_id: str, price: float, count: int):
        """
        Process a customer purchase and store it in DynamoDB
        
        Args:
            customer_id (str): Unique identifier for the customer
            price (float): Price of the purchase
            count (int): Number of items purchased
        """
        timestamp = datetime.utcnow().isoformat()
        
        try:
            # Update DynamoDB with the purchase information
            response = self.table.put_item(
                Item={
                    'customer_id': customer_id,  # Partition key
                    'timestamp': timestamp,
                    'price': price,
                    'count': count
                }
            )
            return {
                'statusCode': 200,
                'body': f'Successfully processed purchase for customer {customer_id}'
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': f'Error processing purchase: {str(e)}'
            }

# Example usage
if __name__ == '__main__':
    processor = CustomerPurchaseProcessor()
    result = processor.process_purchase(
        customer_id="12345",
        price=99.99,
        count=2
    )
    print(result)