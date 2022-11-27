import json
import random
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    
    tenant_id = random.choice(["UTEC", "UNIV2"])
    
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table_alumnos = dynamodb.Table('proyecto_alumnos')
    response = table_alumnos.query(
        KeyConditionExpression=Key('tenant_id').eq(tenant_id)
    )
    
    alumno = random.choice(response['Items'])
    
    id_alumno = alumno["id_alumno"]
    
    # Simulacion de datos
    presion_arterial = random.randint(100, 170) # 110 - 160
    latidos_por_minuto = random.randint(69, 90) # 72 - 86
    saturacion_oxigeno = random.randint(89, 100) # 92 a mas
    now = datetime.now()

    registro = {
        'tenant_id': tenant_id,
        'alumno_id': id_alumno,
        'fecha': str(now.date()),
        'hora': str(now.time()),
        'fecha_hora': str(now.date()) + "//" + str(now.time()),
        'datos_salud': {
            'presion_arterial': presion_arterial,
            'latidos_por_minuto': latidos_por_minuto,
            'saturacion_de_oxigeno': saturacion_oxigeno
        }   
    }
    
    # Publicar en SNS
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
        TopicArn = 'arn:aws:sns:us-east-1:953091505136:NotificarAnomaliaSalud',
        Subject = 'Cuida tu salud!',
        Message = json.dumps(registro),
        MessageAttributes = {
            'tenant_id': {'DataType': 'String', 'StringValue': tenant_id },
            'id_alumno': {'DataType': 'String', 'StringValue': id_alumno },
            'presion_arterial': {'DataType': 'Number', 'StringValue': str(presion_arterial)},
            'latidos_por_minuto': {'DataType': 'Number', 'StringValue': str(latidos_por_minuto)},
            'saturacion_de_oxigeno': {'DataType': 'Number', 'StringValue': str(saturacion_oxigeno)}
        }
    )
    
    # Salida (json)
    return {
        'statusCode': 200,
        'body': response_sns
    }