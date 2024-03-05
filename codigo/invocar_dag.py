from airflow.api.client.local_client import Client

c = Client(None, None)
c.trigger_dag(dag_id='servico_usuarios_mensagens', run_id='invocando_dag1', conf={'usuario_id':1})