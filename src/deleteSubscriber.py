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
        return {
            'statusCode': 500, 
            'body': {'error de conexion en dynamodb'}
        }
    # extract body from request
    body = json.loads(event['body'])
    cellphone_number = body['telefono_celular'] if 'telefono_celular' in body else None
    # validations
    if cellphone_number and not re.match(r'^\d{10}$', cellphone_number) or not cellphone_number:
        return {
            "statusCode": 400,
            "body": json.dumps({"msg":"El numero de celular del suscriptor es necesario y debe contener 10 digitos."})
        }
    existing_subscriber = table.get_item(
        Key={
            "telefono_celular": cellphone_number,
        }
    )
    if 'Item' not in existing_subscriber:
        return {
            "statusCode": 400,
            "body": json.dumps({"msg":f"No existe un suscriptor con el numero de telefono {cellphone_number}."})
        }    
    # delete subscriber
    table.delete_item(
        Key={
            "telefono_celular": cellphone_number,
        }
    )
    response = {
        "statusCode": 200, 
        "body": json.dumps({"msg": f"El suscriptor con el telefono celular {cellphone_number} ha sido eliminado con exito!"})
    }

    return response