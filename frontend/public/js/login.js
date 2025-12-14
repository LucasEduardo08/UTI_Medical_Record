const form = document.getElementById("login-form");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const endereco = document.getElementById("login-endereco").value;
    const privateKey = document.getElementById("login-private-key").value;

    const result = await authService.login(endereco, privateKey);

    if (result.success) {
        // 👇 AQUI entra o redirect
        window.location.href = "/pages/dashboard.html";
    } else {
        document.getElementById("login-error").innerText = result.error;
    }
});
