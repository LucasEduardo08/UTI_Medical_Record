from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('GANACHE_URL')))
        self.contract_address = os.getenv('CONTRACT_ADDRESS')
        
        # Carregar ABI do contrato
        with open('../build/contracts/ProntuarioUTI.json', 'r') as f:
            contract_json = json.load(f)
            self.contract_abi = contract_json['abi']
        
        if self.contract_address:
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=self.contract_abi
            )
    
    def is_connected(self):
        return self.w3.is_connected()
    
    def criar_usuario(self, admin_address, admin_key, novo_endereco, nome, cargo):
        try:
            nonce = self.w3.eth.get_transaction_count(admin_address)
            
            txn = self.contract.functions.criarUsuario(
                novo_endereco,
                nome,
                cargo
            ).build_transaction({
                'from': admin_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(txn, admin_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {'success': True, 'tx_hash': tx_hash.hex()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def obter_usuario(self, endereco):
        try:
            usuario = self.contract.functions.usuarios(endereco).call()
            return {
                'enderecoCarteira': usuario[0],
                'nome': usuario[1],
                'cargo': usuario[2],
                'ativo': usuario[3],
                'dataCriacao': usuario[4]
            }
        except Exception as e:
            print(e)
            return None

    def obter_todos_usuarios(self):
        enderecos = self.contract.functions.obterTodosUsuarios().call()
        usuarios = []

        for endereco in enderecos:
            u = self.obter_usuario(endereco)
            if u and u['ativo']:
                usuarios.append(u)

        return usuarios

    def criar_paciente(self, user_address, user_key, nome, cpf, diagnostico):
        try:
            nonce = self.w3.eth.get_transaction_count(user_address)
            
            txn = self.contract.functions.criarPaciente(
                nome,
                cpf,
                diagnostico
            ).build_transaction({
                'from': user_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(txn, user_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {'success': True, 'tx_hash': tx_hash.hex()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def adicionar_registro(
        self,
        user_address,
        user_key,
        paciente_id,
        tipo_registro,
        descricao,
        sinais_vitais,
        medicamentos
    ):
        try:
            nonce = self.w3.eth.get_transaction_count(user_address)
            
            txn = self.contract.functions.adicionarRegistro(
                paciente_id,
                tipo_registro,
                descricao,
                sinais_vitais,
                medicamentos
            ).build_transaction({
                'from': user_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(txn, user_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {'success': True, 'tx_hash': tx_hash.hex()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def obter_paciente(self, paciente_id):
        try:
            paciente = self.contract.functions.pacientes(paciente_id).call()

            return {
                'id': paciente[0],
                'nome': paciente[1],
                'cpf': paciente[2],
                'dataInternacao': paciente[3],
                'diagnostico': paciente[4],
                'ativo': paciente[5],
            }
        except Exception as e:
            print(e)
            return None
    
    def obter_todos_pacientes(self):
        todos_pacientes = []
        try:
            total = self.contract.functions.totalPacientes().call()  # pega o total de pacientes
            for paciente_id in range(1, 100):  # IDs começam em 1
                paciente = self.obter_paciente(paciente_id)
                if paciente is not None and paciente['ativo']:
                    todos_pacientes.append(paciente)
            return todos_pacientes
        except Exception as e:
            print(e)
            return []
    
    def obter_registros_paciente(self, paciente_id):
        try:
            registro_ids = self.contract.functions.obterRegistrosPaciente(paciente_id).call()
            registros = []
            
            for reg_id in registro_ids:
                registro = self.contract.functions.registros(reg_id).call()
                
                registros.append({
                    'id': registro[0],
                    'pacienteId': registro[1],
                    'medicoResponsavel': registro[2],
                    'tipoRegistro': registro[3],
                    'descricao': registro[4],
                    'sinaisVitais': registro[5],
                    'medicamentos': registro[6],
                    'timestamp': registro[7],
                })
            
            return registros
        except Exception as e:
            print(e)
            return []
    
    def obter_usuario(self, endereco):
        try:
            usuario = self.contract.functions.obterUsuario(endereco).call()
            return {
                'enderecoCarteira': usuario[0],
                'nome': usuario[1],
                'cargo': usuario[2],
                'ativo': usuario[3],
                'dataCriacao': usuario[4],
            }
        except Exception as e:
            print(e)
            return None
