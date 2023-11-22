# Python
import json
import re
# AWS
import boto3


def handler(event, context):
    # connection to dynamodb
    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('Suscriptores')

    except Exception as e:
        return {'statusCode': 500, 'body': {'error de conexion en dynamodb'}}
    # extract cellphone from query string parameters
    parameters = event.get('queryStringParameters', None)
    cellphone_number = parameters['telefono_celular'] if isinstance(parameters, dict) and 'telefono_celular' in parameters else None
    # validations
    if cellphone_number and not re.match(r'^\d{10}$', cellphone_number):
        return {
            "statusCode": 400,
            "body": json.dumps({"msg":"El numero de celular debe contener 10 digitos."})
        }
    # search a subscriber
    if cellphone_number:
        subscriber = table.get_item(
            Key={
                "telefono_celular": cellphone_number,
            }
        )
        subscriber = subscriber.get('Item', {})
        if 'edad' in subscriber:
            subscriber['edad'] = int(subscriber['edad'])
        response = {
                "statusCode": 200,
                "body": json.dumps(subscriber)
        }
    # search for all subscribers      
    else:
        subscribers = table.scan()
        subscribers_list = subscribers.get('Items', [])
        for subscriber in subscribers_list:
            if 'edad' in subscriber:
                subscriber['edad'] = int(subscriber['edad'])

        response = {
                "statusCode": 200,
                "body": json.dumps(subscribers_list)
        }

    return response