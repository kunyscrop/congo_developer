/* --- script.js --- */

// Vérifier si l'utilisateur est connecté au chargement de la page
document.addEventListener("DOMContentLoaded", () => {
    const isConnected = localStorage.getItem("cuber_connected");
    updateInterface(isConnected === "true");
});

function handleAuth(e, isLogin) {
    e.preventDefault();
    // Simulation de connexion réussie
    localStorage.setItem("cuber_connected", "true");
    alert(isLogin ? "Ravi de vous revoir !" : "Bienvenue dans la Cuber Family !");
    window.location.href = "index.html"; // Redirection vers l'accueil
}

function logout() {
    localStorage.removeItem("cuber_connected");
    alert("Déconnexion réussie.");
    window.location.href = "login.html";
}

function updateInterface(connected) {
    const btnLogin = document.getElementById('btn-login-pc');
    const btnLogout = document.getElementById('btn-logout-pc');

    if (!btnLogin || !btnLogout) return; // Sécurité si les boutons n'existent pas

    if(connected) {
        btnLogin.classList.add('hidden');
        btnLogout.classList.remove('hidden');
    } else {
        btnLogin.classList.remove('hidden');
        btnLogout.classList.add('hidden');
    }
}