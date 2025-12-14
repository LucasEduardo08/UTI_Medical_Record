document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-novo-paciente");

    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const nome = document.getElementById("paciente-nome").value;
        const cpf = document.getElementById("paciente-cpf").value;
        const diagnostico = document.getElementById("paciente-diagnostico").value;
        const privateKey = document.getElementById("paciente-private-key").value;

        const token = localStorage.getItem("token");

        try {
            const response = await fetch("http://localhost:5000/api/pacientes", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    nome,
                    cpf,
                    diagnostico,
                    privateKey
                })
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || "Erro ao cadastrar paciente");
                return;
            }

            alert("✅ Paciente cadastrado com sucesso!");
            window.location.href = "/pages/dashboard.html";

        } catch (err) {
            alert("Erro de conexão com o servidor");
        }
    });
});
