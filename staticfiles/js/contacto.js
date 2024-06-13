document.addEventListener("DOMContentLoaded", () => {
  const submitButton = document.querySelector(".enviar");
  submitButton.addEventListener("click", submitFormRegister);
  // Añadir eventos de escucha a los campos del formulario
  addFieldListeners();
});

// Añadir eventos de escucha a los campos del formulario
function addFieldListeners() {
  const form = document.querySelector(".form-contact");
  form.querySelectorAll("input, textarea").forEach((element) => {
    element.addEventListener("input", () => {
      const fieldName = element.name;
      const fieldValue = element.value.trim();
      validateField(fieldName, fieldValue);
    });
  });
}

// Función para limpiar los mensajes de error de un campo específico
function clearFieldError(fieldName) {
  const field = document.querySelector(`[name="${fieldName}"]`); // Buscar cualquier elemento con el atributo name igual a fieldName
  if (field) {
    const groupDiv = field.closest(".group");
    const errorContainer = groupDiv.querySelector(".error-message");
    if (errorContainer) {
      errorContainer.remove();
      field.classList.remove("is-invalid");
    }
  }
}

function validateField(fieldName, fieldValue) {
  clearFieldError(fieldName);

  if (fieldName === "nombre") {
    if (!fieldValue) {
      showFieldError(fieldName, "El campo nombre de usuario es obligatorio");
    }
  }

  if (fieldName === "email") {
    if (!fieldValue) {
      showFieldError(fieldName, "El campo correo electrónico es obligatorio");
    } else if (!isValidEmail(fieldValue)) {
      showFieldError(fieldName, "Formato de correo electrónico inválido");
    }
  }

  if (fieldName === "telefono") {
    if (!fieldValue) {
      showFieldError(fieldName, "El campo teléfono es obligatorio");
    } else if (!isValidPhone(fieldValue)) {
      showFieldError(fieldName, "Formato de teléfono inválido");
    }
  }

  if (fieldName === "mensaje") {
    if (!fieldValue) {
      showFieldError(fieldName, "El campo mensaje es obligatorio");
    }
  }

}

function isValidEmail(email) {
  const commonDomains = ["gmail", "hotmail", "outlook", "yahoo", "aol"]; // Agrega otros dominios comunes si es necesario
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // Dividir el correo electrónico en nombre de usuario y dominio
  const parts = email.split("@");
  if (parts.length !== 2) {
    return false; // El correo electrónico no tiene un formato válido
  }

  const domain = parts[1];
  if (!emailRegex.test(email)) {
    return false; // El formato del correo electrónico no es válido
  }

  // Verificar si el dominio está en la lista de dominios comunes
  const isValidDomain = commonDomains.some((commonDomain) =>
    domain.includes(commonDomain)
  );
  if (!isValidDomain) {
    return false; // El dominio no es uno de los dominios comunes
  }

  return true; // El correo electrónico es válido
}

function isValidPhone(phone) {
  const phoneRegex = /^[0-9]{9}$/;
  return phoneRegex.test(phone);
}

function isValidPassword(password) {
  const passwordRegex =
    /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&.-])[A-Za-z\d@$!%*#?&.-]{8,}$/;
  return passwordRegex.test(password);
}

function showFieldError(fieldName, errorMessage) {
  const field = document.querySelector(`[name="${fieldName}"]`); // Buscar cualquier elemento con el atributo name igual a fieldName
  if (field) {
    const groupDiv = field.closest(".group");
    let errorContainer = groupDiv.querySelector(".error-message");

    if (!errorContainer) {
      errorContainer = document.createElement("div");
      errorContainer.className = "error-message";
      groupDiv.appendChild(errorContainer);
    }

    errorContainer.innerHTML = errorMessage;
    field.classList.add("is-invalid");
  }
}

function clearErrors() {
  const errorMessages = document.querySelectorAll(".error-message");
  errorMessages.forEach((errorMessage) => errorMessage.remove());

  const fields = document.querySelectorAll("input");
  fields.forEach((field) => field.classList.remove("is-invalid"));
}

function validateFormRegister() {
  clearErrors();
  const form = document.querySelector(".form-contact");
  let isValid = true;

  form.querySelectorAll("input, textarea").forEach((input) => {
    const fieldName = input.name;
    const fieldValue = input.value.trim();

    if (fieldName === "nombre") {
      if (!fieldValue) {
        isValid = false;
        showFieldError(fieldName, "El campo nombre de usuario es obligatorio");
      }
    }

    if (fieldName === "email" && !isValidEmail(fieldValue)) {
      isValid = false;
      showFieldError(fieldName, "Formato de correo electrónico inválido");
    }

    if (fieldName === "telefono" && !isValidPhone(fieldValue)) {
      isValid = false;
      showFieldError(fieldName, "Formato de teléfono inválido");
    }

    if (fieldName === "mensaje") {
      if (!fieldValue) {
        isValid = false;
        showFieldError(fieldName, "El campo mensaje es obligatorio");
      }
    }
  });

  return isValid;
}

/*=============== ENVIO DE FORMULARIO ===============*/
function submitFormRegister(event) {
  event.preventDefault();
  if (validateFormRegister()) {
    // Validar el formulario
    const form = document.querySelector(".form-contact");

    Swal.fire({
      icon: "success",
      title: "¡Formulario válido!",
      text: "Enviando datos...",
      showConfirmButton: false,
      timer: 1500,
    });

    // Enviar el formulario
    form.submit();
  } else {
    Swal.fire({
      icon: "error",
      title: "Error",
      text: "Por favor, corrige los errores en el formulario antes de enviarlo.",
    });
    console.log("Formulario inválido. No se puede enviar.");
  }
}