


document.addEventListener("DOMContentLoaded", function() {

    const password = document.getElementById("password");
    const confirm = document.getElementById("password_confirmation");
    const submitBtn = document.querySelector("input[type='submit']");
    const feedback = document.getElementById("password-feedback");

    function validatePasswords() {
        const value = password.value;
        const confirmValue = confirm.value;
        let message = "";
        let isValid = true;
        if (value.length < 8) {
            message = "A senha deve ter pelo menos 8 caracteres.";
            isValid = false;
        } else if (!/[a-z]/i.test(value)) {
            message = "A senha precisa conter pelo menos uma letra.";
            isValid = false;
        } else if (!/[0-9]/.test(value)) {
            message = "A senha precisa conter pelo menos um número.";
            isValid = false;
        } else if (confirmValue && value !== confirmValue) {
            message = "As senhas não coincidem.";
            isValid = false;
        }
        
        if (!isValid) {
            feedback.textContent = message;
            feedback.className = "small text-danger mt-1";
            password.classList.add("is-invalid");
            confirm.classList.add("is-invalid");
            password.classList.remove("is-valid");
            confirm.classList.remove("is-valid");
            submitBtn.disabled = true;
        } else if (value && confirmValue) {
            feedback.textContent = "Senha válida";
            feedback.className = "small text-success mt-1";
            password.classList.remove("is-invalid");
            confirm.classList.remove("is-invalid");
            password.classList.add("is-valid");
            confirm.classList.add("is-valid");
            submitBtn.disabled = false;
        } else {
            feedback.textContent = "";
            password.classList.remove("is-valid", "is-invalid");
            confirm.classList.remove("is-valid", "is-invalid");
            submitBtn.disabled = false;
        }
    }
    
    password.addEventListener("input", validatePasswords);
    confirm.addEventListener("input", validatePasswords);
});