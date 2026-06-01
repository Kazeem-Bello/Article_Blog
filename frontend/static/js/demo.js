// register alternative


const registerForm = document.getElementById("registerForm");

const emailInput = document.getElementById("email");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");


const emailError = document.getElementById("emailError");
const usernameError = document.getElementById("usernameError");
const passwordError = document.getElementById("passwordError");
const messageDiv = document.getElementById("message");

function clearErrors() {
  emailError.textContent = "";
  usernameError.textContent = "";
  passwordError.textContent = "";
  messageDiv.innerHTML = "";
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isStrongPassword(password) {
  const hasMinLength = password.length >= 8;
  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  const hasSpecialCharacter = /[^A-Za-z0-9]/.test(password);

  return (
    hasMinLength &&
    hasUppercase &&
    hasLowercase &&
    hasNumber &&
    hasSpecialCharacter
  );
}

function validateForm() {
  clearErrors();

  let isValid = true;

  const email = emailInput.value.trim();
  const username = usernameInput.value.trim();
  const password = passwordInput.value;


  if (!email) {
    emailError.textContent = "Email is required.";
    isValid = false;
  } else if (!isValidEmail(email)) {
    emailError.textContent = "Enter a valid email address.";
    isValid = false;
  }

  if (!username) {
    usernameError.textContent = "Username is required.";
    isValid = false;
  } else if (username.length < 3) {
    usernameError.textContent = "Username must be at least 3 characters long.";
    isValid = false;
  }

  if (!password) {
    passwordError.textContent = "Password is required.";
    isValid = false;
  } else if (!isStrongPassword(password)) {
    passwordError.textContent =
      "Must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number and one special character.";
    isValid = false;
  }
  return isValid;
}

registerForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  if (!validateForm()) {
    return;
  }

  const userData = {
    email: emailInput.value.trim(),
    username: usernameInput.value.trim(),
    password: passwordInput.value
  };

  try {
    const response = await fetch("/api/v1/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(userData)
    });

    const data = await response.json();

    if (!response.ok) {
      messageDiv.innerHTML = `
        <div class="alert alert-danger">
          ${data.detail || "Registration failed. Please try again."}
        </div>
      `;
      return;
    }

    messageDiv.innerHTML = `
      <div class="alert alert-success">
        Account created successfully. Redirecting to login...
      </div>
    `;

    registerForm.reset();

    setTimeout(() => {
      window.location.href = "/login.html";
    }, 1500);

  } catch (error) {
    messageDiv.innerHTML = `
      <div class="alert alert-danger">
        Something went wrong. Please try again.
      </div>
    `;
  }
});

document.querySelectorAll(".toggle-password").forEach((button) => {
  button.addEventListener("click", function () {
    const targetId = this.getAttribute("data-target");
    const input = document.getElementById(targetId);

    if (input.type === "password") {
      input.type = "text";
    } else {
      input.type = "password";
    }
  });
});