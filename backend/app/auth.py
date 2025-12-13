import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import os

JWT_SECRET = os.getenv('JWT_SECRET', 'seu_segredo_aqui')

def gerar_token(endereco, nome, cargo):
    payload = {
        'endereco': endereco,
        'nome': nome,
        'cargo': cargo,
        'exp': datetime.utcnow() + timedelta(hours=8)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verificar_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Token não fornecido'}), 401

        try:
            # Esperado: "Bearer <token>"
            token = token.split(' ')[1]
            payload = verificar_token(token)

            if not payload:
                return jsonify({'error': 'Token inválido'}), 401

            request.user = payload

        except Exception as e:
            return jsonify({'error': 'Token inválido'}), 401

        return f(*args, **kwargs)

    return decorated
