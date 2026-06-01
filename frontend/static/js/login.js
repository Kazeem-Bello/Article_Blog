const registerForm = document.getElementById("loginForm");
const messageDiv = document.getElementById("message");
const submitButton = registerForm.querySelector('button[type="submit"]');

const email = document.getElementById("email");
const password = document.getElementById("password");

function showError(message) {
  messageDiv.innerHTML = `
    <div class="alert alert-danger" role="alert">
      ${message}
    </div>
  `;
}

function showSuccess(message) {
  messageDiv.innerHTML = `
    <div class="alert alert-success role="alert">
      ${message}
    </div>
  `;
}

function formatBackendError(data) {
  if (Array.isArray(data.detail)) {
    return data.detail
      .map((error) => {
        const field = error.loc ? error.loc[error.loc.length - 1] : "field";
        return `${field}: ${error.msg}`;
      })
      .join("<br>");
  }

  return data.detail || "Login failed";
}

registerForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  messageDiv.innerHTML = "";

  const userData = {
    email: email.value.trim(),
    password: password.value,
  };

  // submitButton.disabled = true;
  submitButton.innerHTML = "Signing in...";

  try {
    const response = await fetch("/api/v1/auth/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    });

    const data = await response.json();

    if (!response.ok) {
      const errorMessage = formatBackendError(data);
      showError(errorMessage);
      return;
    }

    showSuccess("You have successfully logged in.");

    loginForm.reset();

    // setTimeout(() => {
    //   window.location.href = "/login.html";
    // }, 1500);
  } catch (error) {
    showError("Something went wrong. Please try again.");
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = "Sign in";
  }
});
