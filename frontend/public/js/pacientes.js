document.addEventListener("DOMContentLoaded", async () => {
    const lista = document.getElementById("pacientes-lista");
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Usuário não autenticado");
        window.location.href = "/pages/login.html";
        return;
    }

    lista.innerHTML = "<p>Carregando pacientes...</p>";

    try {
        const response = await fetch("http://localhost:5000/api/obterpacientes", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const pacientes = await response.json();

        if (!response.ok) {
            lista.innerHTML = "<p>Erro ao carregar pacientes</p>";
            return;
        }

        if (pacientes.length === 0) {
            lista.innerHTML = "<p>Nenhum paciente cadastrado</p>";
            return;
        }

        lista.innerHTML = "";

        pacientes.forEach(p => {
            const card = document.createElement("div");
            card.className = "card";
            card.innerHTML = `
                <h3>${p.nome}</h3>
                <p><strong>CPF:</strong> ${p.cpf}</p>
                <p><strong>Diagnóstico:</strong> ${p.diagnostico}</p>
                <p><strong>Internação:</strong> ${new Date(p.dataInternacao * 1000).toLocaleDateString()}</p>
            `;
            lista.appendChild(card);
        });

    } catch (err) {
        lista.innerHTML = "<p>Erro de conexão com o servidor</p>";
    }
});
