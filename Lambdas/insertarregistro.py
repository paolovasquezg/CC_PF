import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    body = json.loads(event['Records'][0]['body'])
    registro = json.loads(body['Message'])
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('proyectoinformacionsalud')
    response_table = table.put_item(Item=registro)
    return {
        'statusCode': 200,
        'response': response_table
    }
