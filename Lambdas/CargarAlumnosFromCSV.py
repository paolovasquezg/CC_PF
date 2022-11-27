import urllib.parse
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    s3 = boto3.client('s3')
    lines =[linea for linea in s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode('ascii').split('\r\n')]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('proyecto_alumnos')
    
    for linea in lines:
        datos = linea.split(",")
        alumno = {
          "tenant_id": datos[0],
          "id_alumno": datos[1],
          "alumno_datos": {
            "nombre": datos[10],
            "sexo": datos[9],
            "fecha_nac": datos[2],
            "celular": datos[3],
            "domicilio": {
              "direcc": datos[4],
              "distrito": datos[5],
              "provincia": datos[6],
              "departamento": datos[7],
              "pais": datos[8]
            }
          }
        }
        
        table.put_item(Item=alumno)
        
    
    # Salida (json)
    
    return {
        'statusCode': 200
    }