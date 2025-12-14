document.addEventListener('DOMContentLoaded', () => {
    // Verificar autenticação
    if (authService.isAuthenticated()) {
        mostrarDashboard();
    }

    // Login
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const endereco = document.getElementById('login-endereco').value;
        const privateKey = document.getElementById('login-private-key').value;

        const resultado = await authService.login(endereco, privateKey);
        
        if (resultado.success) {
            mostrarDashboard();
        } else {
            document.getElementById('login-error').textContent = resultado.error;
        }
    });

    // Logout
    document.getElementById('logout-btn').addEventListener('click', () => {
        authService.logout();
        mostrarLogin();
    });

    // Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(`tab-${tab}`).classList.add('active');
        });
    });

    // Novo Paciente
    document.getElementById('form-novo-paciente').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const nome = document.getElementById('paciente-nome').value;
        const cpf = document.getElementById('paciente-cpf').value;
        const diagnostico = document.getElementById('paciente-diagnostico').value;
        const privateKey = document.getElementById('paciente-private-key').value;

        const resultado = await blockchainAPI.criarPaciente(nome, cpf, diagnostico, privateKey);
        
        if (resultado.success) {
            alert('Paciente cadastrado com sucesso!');
            e.target.reset();
            prontuarioManager.carregarPacientes();
        } else {
            alert('Erro: ' + resultado.error);
        }
    });

    // Novo Usuário
    document.getElementById('form-novo-usuario').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const endereco = document.getElementById('usuario-endereco').value;
        const nome = document.getElementById('usuario-nome').value;
        const cargo = document.getElementById('usuario-cargo').value;

        const resultado = await blockchainAPI.criarUsuario(endereco, nome, cargo);
        
        if (resultado.success) {
            alert('Usuário criado com sucesso!');
            e.target.reset();
        } else {
            alert('Erro: ' + resultado.error);
        }
    });

    // Novo Registro
    document.getElementById('form-novo-registro').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const tipo = document.getElementById('registro-tipo').value;
        const descricao = document.getElementById('registro-descricao').value;
        const sinais = document.getElementById('registro-sinais').value;
        const medicamentos = document.getElementById('registro-medicamentos').value;
        const privateKey = document.getElementById('registro-private-key').value;

        const resultado = await blockchainAPI.adicionarRegistro(
            prontuarioManager.pacienteAtual.id,
            tipo,
            descricao,
            sinais,
            medicamentos,
            privateKey
        );
        
        if (resultado.success) {
            alert('Registro adicionado com sucesso!');
            e.target.reset();
            prontuarioManager.carregarRegistros(prontuarioManager.pacienteAtual.id);
        } else {
            alert('Erro: ' + resultado.error);
        }
    });

    // Fechar Modal
    document.querySelector('.close').addEventListener('click', () => {
        document.getElementById('modal-paciente').classList.remove('active');
    });
});

function mostrarLogin() {
    document.getElementById('login-screen').classList.add('active');
    document.getElementById('dashboard-screen').classList.remove('active');
}

function mostrarDashboard() {
    document.getElementById('login-screen').classList.remove('active');
    document.getElementById('dashboard-screen').classList.add('active');
    
    const user = authService.user;
    document.getElementById('user-name').textContent = user.nome;
    document.getElementById('user-cargo').textContent = user.cargo;
    
    // Esconder tab de usuários se não for admin
    if (user.cargo !== 'Admin') {
        document.getElementById('tab-usuarios').style.display = 'none';
    }
    
    prontuarioManager.carregarPacientes();
}