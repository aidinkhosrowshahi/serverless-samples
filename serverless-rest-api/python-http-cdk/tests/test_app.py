from src.app import lambda_handler
from unittest.mock import patch, MagicMock
import json
import pytest

class TestApp:

    @pytest.fixture
    def mock_table(self):
        with patch('src.app.table') as mock:
            yield mock

    def test_lambda_handler_2(self):
        """
        Test lambda_handler with all required fields present
        """
        # Arrange
        event = {
            'body': {
                'customer_id': 'customer456',
                'timestamp': '2023-04-16T14:30:00Z',
                'price': 149.99,
                'count': 1,
                'item': 'Product ABC'
            }
        }
        context = {}

        # Mock the DynamoDB table
        with patch('src.app.table') as mock_table:
            mock_table.put_item = MagicMock()

            # Act
            response = lambda_handler(event, context)

        # Assert
        assert response['statusCode'] == 200
        assert json.loads(response['body']) == {'message': 'Sales item processed successfully'}
        
        mock_table.put_item.assert_called_once_with(Item={
            'customer_id': 'customer456',
            'timestamp': '2023-04-16T14:30:00Z',
            'price': 149.99,
            'count': 1,
            'item': 'Product ABC'
        })

    def test_lambda_handler_dynamodb_exception(self, mock_table):
        """
        Test lambda_handler when DynamoDB throws an exception
        """
        event = {'body': json.dumps({
            'customer_id': '123',
            'timestamp': '2023-04-20T12:00:00Z',
            'price': 10.99,
            'count': 1,
            'item': 'test_item'
        })}
        context = {}
        mock_table.put_item.side_effect = Exception("DynamoDB error")
        response = lambda_handler(event, context)
        assert response['statusCode'] == 500
        assert json.loads(response['body'])['error'] == 'DynamoDB error'

    def test_lambda_handler_empty_input(self, mock_table):
        """
        Test lambda_handler with empty input
        """
        event = {}
        context = {}
        response = lambda_handler(event, context)
        assert response['statusCode'] == 400
        assert json.loads(response['body'])['error'] == 'Missing required field: customer_id'

    @patch('src.app.table')
    def test_lambda_handler_exception_handling(self, mock_table):
        """
        Test lambda_handler when an exception occurs during processing.
        """
        # Arrange
        event = {
            'body': json.dumps({
                'customer_id': 'test_customer',
                'timestamp': '2023-05-01T12:00:00Z',
                'price': 10.99,
                'count': 1,
                'item': 'test_item'
            })
        }
        context = MagicMock()
        mock_table.put_item.side_effect = Exception("Test exception")

        # Act
        response = lambda_handler(event, context)

        # Assert
        assert response['statusCode'] == 500
        assert json.loads(response['body']) == {'error': 'Test exception'}

    def test_lambda_handler_invalid_input_type(self, mock_table):
        """
        Test lambda_handler with invalid input type
        """
        event = {'body': json.dumps({
            'customer_id': '123',
            'timestamp': '2023-04-20T12:00:00Z',
            'price': 'invalid',  # Should be a number
            'count': 1,
            'item': 'test_item'
        })}
        context = {}
        response = lambda_handler(event, context)
        assert response['statusCode'] == 500
        assert 'error' in json.loads(response['body'])

    def test_lambda_handler_invalid_timestamp_format(self, mock_table):
        """
        Test lambda_handler with invalid timestamp format
        """
        event = {'body': json.dumps({
            'customer_id': '123',
            'timestamp': 'invalid_timestamp',
            'price': 10.99,
            'count': 1,
            'item': 'test_item'
        })}
        context = {}
        response = lambda_handler(event, context)
        assert response['statusCode'] == 200  # The function doesn't validate timestamp format
        assert json.loads(response['body'])['message'] == 'Sales item processed successfully'

    def test_lambda_handler_missing_required_field(self):
        """
        Test lambda_handler when a required field is missing from the request body.
        """
        # Arrange
        event = {
            'body': json.dumps({
                'customer_id': 'test_customer',
                'timestamp': '2023-05-01T12:00:00Z',
                'price': 10.99,
                'count': 1
                # 'item' field is missing
            })
        }
        context = MagicMock()

        # Act
        response = lambda_handler(event, context)

        # Assert
        assert response['statusCode'] == 400
        assert json.loads(response['body']) == {'error': 'Missing required field: item'}

    def test_lambda_handler_missing_required_field_2(self, mock_table):
        """
        Test lambda_handler with missing required field
        """
        event = {'body': json.dumps({
            'customer_id': '123',
            'timestamp': '2023-04-20T12:00:00Z',
            'price': 10.99,
            'count': 1
            # 'item' is missing
        })}
        context = {}
        response = lambda_handler(event, context)
        assert response['statusCode'] == 400
        assert json.loads(response['body'])['error'] == 'Missing required field: item'

    def test_lambda_handler_non_json_body(self, mock_table):
        """
        Test lambda_handler with non-JSON body
        """
        event = {'body': 'This is not JSON'}
        context = {}
        response = lambda_handler(event, context)
        assert response['statusCode'] == 500
        assert 'error' in json.loads(response['body'])

    @patch('src.app.table')
    def test_lambda_handler_successful_processing(self, mock_table):
        """
        Test successful processing of a sales item in lambda_handler
        """
        # Arrange
        event = {
            'body': json.dumps({
                'customer_id': 'customer123',
                'timestamp': '2023-04-15T12:00:00Z',
                'price': 99.99,
                'count': 2,
                'item': 'Product XYZ'
            })
        }
        context = {}

        mock_table.put_item = MagicMock()

        # Act
        response = lambda_handler(event, context)

        # Assert
        assert response['statusCode'] == 200
        assert json.loads(response['body']) == {'message': 'Sales item processed successfully'}
        
        mock_table.put_item.assert_called_once_with(Item={
            'customer_id': 'customer123',
            'timestamp': '2023-04-15T12:00:00Z',
            'price': 99.99,
            'count': 2,
            'item': 'Product XYZ'
        })

    @patch('src.app.table')
    def test_lambda_handler_successful_processing_2(self, mock_table):
        """
        Test lambda_handler when all required fields are present and processing is successful.
        """
        # Arrange
        event = {
            'body': json.dumps({
                'customer_id': 'test_customer',
                'timestamp': '2023-05-01T12:00:00Z',
                'price': 10.99,
                'count': 1,
                'item': 'test_item'
            })
        }
        context = MagicMock()

        # Act
        response = lambda_handler(event, context)

        # Assert
        assert response['statusCode'] == 200
        assert json.loads(response['body']) == {'message': 'Sales item processed successfully'}
        mock_table.put_item.assert_called_once()