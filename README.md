# 🏥 Prontuário Médico UTI com Blockchain

## 📌 Descrição do Projeto

Este projeto tem como objetivo o desenvolvimento de um **Prontuário Médico para Unidade de Terapia Intensiva (UTI)** utilizando **Blockchain** como camada principal de segurança, integridade e auditoria dos dados.

A aplicação permite:

* Cadastro de **usuários do sistema** (administradores, médicos, etc.)
* Cadastro de **pacientes**
* Registro de **anotações médicas** (evoluções, sinais vitais, medicamentos)
* Garantia de que apenas **usuários autorizados** possam acessar e modificar os dados

O sistema é composto por três partes principais:

* **Smart Contract (Solidity)**: responsável por armazenar e validar os dados na blockchain
* **Backend (Python + Flask)**: faz a comunicação entre o frontend e a blockchain
* **Frontend (React + HTML/JS)**: interface gráfica para interação com o sistema

A blockchain utilizada é uma **rede local Ethereum**, executada com **Ganache**, e os contratos são gerenciados com **Truffle**.

---

## 🧱 Tecnologias Utilizadas

* **Blockchain / Smart Contracts**: Solidity, Truffle
* **Rede Ethereum Local**: Ganache
* **Backend**: Python, Flask, Web3.py
* **Frontend**: React, HTML, CSS, JavaScript
* **Controle de versão**: Git e GitHub

---

## ⚙️ Passo a Passo para Executar o Projeto

### 1️⃣ Pré-requisitos

#### Instalar Node.js e npm

* Baixar em: [https://nodejs.org/](https://nodejs.org/)

Verifique a instalação:

```bash
node -v
npm -v
```

---

### 2️⃣ Instalar Truffle globalmente

```bash
npm install -g truffle
```

Verifique:

```bash
truffle version
```

---

### 3️⃣ Instalar Ganache

* Baixar em: [https://trufflesuite.com/ganache/](https://trufflesuite.com/ganache/)

---

### 4️⃣ Configurar Ganache

1. Abrir o **Ganache**
2. Criar um novo **Workspace**
3. Configurar para rodar na porta **7545**
4. Anotar:

   * Endereço da **primeira conta** (admin)
   * **Chave privada** dessa conta (será usada no backend)

---

### 5️⃣ Compilar e fazer deploy do contrato

Na **raiz do projeto**:

```bash
truffle compile
truffle migrate --reset
```

Após o deploy:

* Anotar o **endereço do contrato** exibido no terminal
* Esse endereço será usado no backend

---

## 🖥️ Backend (Flask + Web3)

### 6️⃣ Configurar o backend

Entrar na pasta backend:

```bash
cd backend
```

Criar ambiente virtual Python:

```bash
python -m venv venv
```

Ativar o ambiente virtual:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / Mac:**

```bash
source venv/bin/activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

---

### 7️⃣ Configurar variáveis de ambiente

Editar o arquivo `backend/.env` com:

* `CONTRACT_ADDRESS` → endereço do contrato gerado pelo Truffle
* `PRIVATE_KEY` → chave privada da conta admin do Ganache

Exemplo:

```env
GANACHE_URL=http://127.0.0.1:7545
CONTRACT_ADDRESS=0x1234567890abcdef...
PRIVATE_KEY=0xabcdef123456...
```

---

### 8️⃣ Executar o backend

Ainda com o ambiente virtual ativado:

```bash
cd app
python main.py
```

O servidor será iniciado em:

👉 **[http://localhost:5000](http://localhost:5000)**

---

## 🌐 Frontend

### 9️⃣ Configurar o frontend

Em outro terminal, ir para a pasta frontend:

```bash
cd frontend
```

Instalar dependências:

```bash
npm install
```

---

### 🔟 Executar o frontend

Opção 1 — Servidor simples com Python:

```bash
cd public
python -m http.server 8000
```

Opção 2 — Live Server:

```bash
npm install -g live-server
live-server public
```

Acessar no navegador:

👉 **[http://localhost:8000](http://localhost:8000)**

---

## 🔐 Observações Importantes

* A **primeira conta do Ganache** é o administrador do sistema
* Apenas o **admin** pode cadastrar novos usuários
* Nunca suba **chaves privadas** ou arquivos `.env` para o GitHub
* A blockchain garante **imutabilidade, rastreabilidade e segurança** dos registros médicos

---

## 📚 Contexto Acadêmico

Este projeto foi desenvolvido como trabalho acadêmico, com foco nos seguintes conceitos:

* Criptografia aplicada
* Blockchain e Smart Contracts
* Segurança da informação
* Desenvolvimento de sistemas distribuídos

---

## 👨‍💻 Autor

Danilo Bruno, Lucas Eduardo e Ian Marcon

Curso: Engenharia de Computação

---

✅ Projeto pronto para execução local utilizando Ganache e Ethereum privado.
