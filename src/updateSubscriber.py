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
    subscriber = body['suscriptor'] if 'suscriptor' in body else {}
    cellphone_number = subscriber['telefono_celular'] if 'telefono_celular' in subscriber else None
    # validations
    if 'nombre' in subscriber and not re.match(r'^\w{3,}$', subscriber['nombre']) or 'nombre' not in subscriber:
        return {
            "statusCode": 400,
            "body": json.dumps({"msg":"El nombre del suscriptor es necesario y debe contener minimo 3 letras."})
        }
    if 'apellido_materno' in subscriber and not re.match(r'^\w{3,}$', subscriber['apellido_materno']) or 'apellido_materno' not in subscriber:
        return {
            "statusCode": 400,
            "body": json.dumps({"msg":"El apellido materno del suscriptor es necesario y debe contener minimo 3 letras."})
        }
    if cellphone_number and not re.match(r'^\d{10}$', cellphone_number) or not cellphone_number:
        return {
            "statusCode": 400,
            "body": json.dumps({"msg":"El numero de celular del suscriptor es necesario y debe contener 10 digitos."})
        }
    if 'edad' in subscriber and not isinstance(subscriber['edad'], int):
        return {
            "statusCode": 400,
            "body": json.dumps({"msg":"La edad del suscriptor debe de ser un numero entero."})
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
    if 'apellido_paterno' not in subscriber:
        subscriber['apellido_paterno'] = ""       
    # update subscriber to dynamo table
    table.put_item(Item=subscriber)
    response = {
        "statusCode": 200, 
        "body": json.dumps({"msg":"Suscriptor actualizado exitosamente!"})
    }

    return response