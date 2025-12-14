// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ProntuarioUTI {
    address[] private listaUsuarios;

    struct Usuario {
        address enderecoCarteira;
        string nome;
        string cargo;
        bool ativo;
        uint256 dataCriacao;
    }
    
    struct Paciente {
        uint256 id;
        string nome;
        string cpf;
        uint256 dataInternacao;
        string diagnostico;
        bool ativo;
    }
    
    struct RegistroMedico {
        uint256 id;
        uint256 pacienteId;
        address medicoResponsavel;
        string tipoRegistro;
        string descricao;
        string sinaisVitais;
        string medicamentos;
        uint256 timestamp;
    }
    
    mapping(address => Usuario) public usuarios;
    mapping(uint256 => Paciente) public pacientes;
    mapping(uint256 => RegistroMedico) public registros;
    mapping(uint256 => uint256[]) public registrosPorPaciente;
    
    address public admin;
    uint256 public totalPacientes;
    uint256 public totalRegistros;
    
    event UsuarioCriado(address indexed endereco, string nome, string cargo);
    event PacienteCriado(uint256 indexed id, string nome, string cpf);
    event RegistroAdicionado(uint256 indexed id, uint256 indexed pacienteId, address indexed medico);
    
    modifier apenasAdmin() {
        require(msg.sender == admin, "Apenas administrador");
        _;
    }
    
    modifier apenasUsuarioAtivo() {
        require(usuarios[msg.sender].ativo, "Usuario nao autorizado");
        _;
    }
        
    constructor() {
        admin = msg.sender;

        usuarios[admin] = Usuario({
            enderecoCarteira: admin,
            nome: "Administrador",
            cargo: "Admin",
            ativo: true,
            dataCriacao: block.timestamp
        });

        listaUsuarios.push(admin); // ESSENCIAL
    }

    
    function criarUsuario(
        address _endereco,
        string memory _nome,
        string memory _cargo
    ) public apenasAdmin {
        require(!usuarios[_endereco].ativo, "Usuario ja existe");

        usuarios[_endereco] = Usuario({
            enderecoCarteira: _endereco,
            nome: _nome,
            cargo: _cargo,
            ativo: true,
            dataCriacao: block.timestamp
        });

        // ESSENCIAL
        listaUsuarios.push(_endereco);

        emit UsuarioCriado(_endereco, _nome, _cargo);
    }

    function criarPaciente(
        string memory _nome,
        string memory _cpf,
        string memory _diagnostico
    ) public apenasUsuarioAtivo returns (uint256) {
        totalPacientes++;
        
        pacientes[totalPacientes] = Paciente({
            id: totalPacientes,
            nome: _nome,
            cpf: _cpf,
            dataInternacao: block.timestamp,
            diagnostico: _diagnostico,
            ativo: true
        });
        
        emit PacienteCriado(totalPacientes, _nome, _cpf);
        return totalPacientes;
    }
    
    function adicionarRegistro(
        uint256 _pacienteId,
        string memory _tipoRegistro,
        string memory _descricao,
        string memory _sinaisVitais,
        string memory _medicamentos
    ) public apenasUsuarioAtivo returns (uint256) {
        require(pacientes[_pacienteId].ativo, "Paciente nao encontrado");
        
        totalRegistros++;
        
        registros[totalRegistros] = RegistroMedico({
            id: totalRegistros,
            pacienteId: _pacienteId,
            medicoResponsavel: msg.sender,
            tipoRegistro: _tipoRegistro,
            descricao: _descricao,
            sinaisVitais: _sinaisVitais,
            medicamentos: _medicamentos,
            timestamp: block.timestamp
        });
        
        registrosPorPaciente[_pacienteId].push(totalRegistros);
        
        emit RegistroAdicionado(totalRegistros, _pacienteId, msg.sender);
        return totalRegistros;
    }
    
    function obterRegistrosPaciente(uint256 _pacienteId) 
        public 
        view 
        apenasUsuarioAtivo 
        returns (uint256[] memory) {
        return registrosPorPaciente[_pacienteId];
    }
    
    function obterUsuario(address _endereco) 
        public 
        view 
        returns (Usuario memory) {
        return usuarios[_endereco];
    }

    function obterTodosUsuarios() public view returns (address[] memory) {
    return listaUsuarios;
    }
    
    function desativarPaciente(uint256 _pacienteId) public apenasUsuarioAtivo {
        require(pacientes[_pacienteId].ativo, "Paciente nao encontrado");
        pacientes[_pacienteId].ativo = false;
    }
}