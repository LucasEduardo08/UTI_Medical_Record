form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const endereco = document.getElementById("usuario-endereco").value;
    const nome = document.getElementById("usuario-nome").value;
    const cargo = document.getElementById("usuario-cargo").value;

    try {
        const response = await fetch("http://localhost:5000/api/usuarios", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ endereco, nome, cargo })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            alert(data.error || "Erro ao cadastrar usuário");
            return;
        }

        alert("✅ Usuário cadastrado com sucesso!");
        form.reset();

    } catch (err) {
        alert("❌ Erro de conexão com o servidor");
    }
});
