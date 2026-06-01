const registerForm = document.getElementById("registerForm");
const messageDiv = document.getElementById("message");
const submitButton = registerForm.querySelector('button[type="submit"]');

const email = document.getElementById("email");
const username = document.getElementById("username");
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
    <div class="alert alert-success">
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

  return data.detail || "Registration failed";
}

registerForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  messageDiv.innerHTML = "";

  const userData = {
    email: email.value.trim(),
    username: username.value.trim(),
    password: password.value,
  };

  // submitButton.disabled = true;
  submitButton.innerHTML = "Creating account...";

  try {
    const response = await fetch("/api/v1/auth/register", {
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

    showSuccess("Registration successful. You can now login.");

    registerForm.reset();

    // setTimeout(() => {
    //   window.location.href = "/login.html";
    // }, 1500);
  } catch (error) {
    showError("Something went wrong. Please try again.");
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = "Sign up";
  }
});
