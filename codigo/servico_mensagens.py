import requests
from flask import Flask, jsonify, request
import py_eureka_client.eureka_client as eureka_client


app = Flask(__name__)

# Registrar o serviço no Eureka:
eureka_client.init(eureka_server="http://localhost:8761/eureka/v2",
                   app_name="servico_mensagens",
                   instance_port=5002)

@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    dados = request.json
    usuario_id = dados.get('usuario_id')
    grupo = dados.get('grupo')
    mensagem = dados.get('mensagem')

    # Simular o envio da mensagem para o grupo

    print(f"Mensagem enviada para o grupo '{grupo}': {mensagem}")
    return jsonify({'mensagem': 'Mensagem enviada com sucesso para o grupo'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5002)
