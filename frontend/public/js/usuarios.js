document.addEventListener("DOMContentLoaded", async () => {
    const lista = document.getElementById("usuarios-lista");
    if (!lista) return;

    try {
        const response = await fetch("http://localhost:5000/api/obterusuarios");
        const usuarios = await response.json();

        if (!Array.isArray(usuarios) || usuarios.length === 0) {
            lista.innerHTML = "<p>Nenhum usuário encontrado.</p>";
            return;
        }

        lista.innerHTML = "";

        usuarios.forEach(u => {
            const card = document.createElement("div");
            card.className = "card";
            card.innerHTML = `
                <h3>${u.nome}</h3>
                <p><strong>Endereço:</strong> ${u.enderecoCarteira}</p>
                <p><strong>Cargo:</strong> ${u.cargo}</p>
            `;
            lista.appendChild(card);
        });

    } catch (err) {
        console.error(err);
        lista.innerHTML = "<p>Erro ao carregar usuários.</p>";
    }
});
