from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models.param import Param
from datetime import datetime, timedelta
import asyncio
import requests
import json
from py_eureka_client import eureka_client

def obter_usuario(**kwargs):
    usuario_id = kwargs['usuario_id']
    print(f"  #################### usuario_id {usuario_id} ####################")
    eureka_client.init(eureka_server="http://localhost:8761/eureka/v2",
                app_name="servico_usuarios",
                instance_port=5001)
    url=f"/usuario/{usuario_id}"
    resposta = eureka_client.do_service("servico_usuarios", url, return_type="response_object",method="GET")
    if resposta.status == 200:
        # Convert bytes to string type and string type to dict
        string = resposta.read().decode('utf-8')
        json_obj = json.loads(string)
        usuario = json_obj
        # Passando dados para a próxima tarefa
        kwargs['ti'].xcom_push(key='usuario', value=usuario)
    else:
        raise ValueError(f"**************************  Usuário {usuario_id} erro {resposta.status}")

def enviar_mensagem(**kwargs):
    ti = kwargs['ti']
    usuario = ti.xcom_pull(key='usuario', task_ids='obter_usuario')
    print(f"  #################### usuario {usuario} ####################")  
    if 'admin' in usuario['grupos']:
        grupo = 'admin'
        eureka_client.init(eureka_server="http://localhost:8761/eureka/v2",
                   app_name="servico_mensagens",
                   instance_port=5002)
        mensagem = {"usuario_id": usuario["id"], "grupo": "admin", "mensagem": "Mensagem automática do Airflow"}
        resposta = eureka_client.do_service("servico_mensagens", "/enviar_mensagem", headers={"Content-type":"application/json"},method="POST", data=json.dumps(mensagem)) 
        print(f"&&&&&&&&&&&&&&&&&&&&&& resposta {resposta} ####################")
    else:
        raise ValueError(f"**************************  Usuário {usuario['nome']} não é administrador")
        print(f"**************************  Usuário {usuario['nome']} não é administrador")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('servico_usuarios_mensagens',
          default_args=default_args,
          params={"usuario_id": Param(1, type="integer", minimum=1)},
          description='Consulta usuário e envia mensagem',
          schedule_interval=timedelta(days=1))
usuario_id="{{ dag_run.conf['usuario_id'] }}"

t1 = PythonOperator(
    task_id='obter_usuario',
    python_callable=obter_usuario,
    op_kwargs={'usuario_id': usuario_id},
    dag=dag,
)

t2 = PythonOperator(
    task_id='enviar_mensagem',
    python_callable=enviar_mensagem,
    dag=dag,
)

t1 >> t2