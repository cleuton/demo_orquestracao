from flask import Flask, jsonify
import py_eureka_client.eureka_client as eureka_client

app = Flask(__name__)

# Simulando uma base de dados de usuários e grupos
usuarios = {
    1: {'id': 1, 'nome': 'João', 'grupos': ['admin', 'moderador']},
    2: {'id': 2, 'nome': 'Maria', 'grupos': ['moderador']},
    3: {'id': 3, 'nome': 'Pedro', 'grupos': ['usuario']}
}

# Registrar o serviço no Eureka:
eureka_client.init(eureka_server="http://localhost:8761/eureka/v2",
                   app_name="servico_usuarios",
                   instance_port=5001)

@app.route('/usuario/<int:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    if usuario_id in usuarios:
        return jsonify(usuarios[usuario_id])
    else:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5001)
