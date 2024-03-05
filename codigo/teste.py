import asyncio
import requests
import json
from py_eureka_client import eureka_client

def enviar(): 
    eureka_client.init(eureka_server="http://localhost:8761/eureka/v2",
                   app_name="servico_mensagens",
                   instance_port=5002)
    mensagem = {"usuario_id": 1, "grupo": "grupo1", "mensagem": "Mensagem automática do Airflow"}
    response = eureka_client.do_service("servico_mensagens", "/enviar_mensagem", headers={"Content-type":"application/json"},method="POST", data=json.dumps(mensagem)) 
    print(response)

if __name__ == "__main__":
    enviar()
