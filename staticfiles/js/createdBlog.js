document.addEventListener("DOMContentLoaded", () => {
  const submitButton = document.querySelector(".enviar");
  submitButton.addEventListener("click", submitFormCreatedBlog);
});

function clearErrors() {
  const errorMessages = document.querySelectorAll(".error-message");
  errorMessages.forEach((errorMessage) => errorMessage.remove());
}

function isValidContentTitle(content) {
  const words = content.trim().split(/\s+/); // Dividir por cualquier espacio en blanco
  return words.length <= 10;
}

function isValidContentDescription(content) {
  const words = content.trim().split(/\s+/); // Dividir por cualquier espacio en blanco
  return words.length <= 22;
}

function isValidContent(content) {
  const words = content.trim().split(/\s+/); // Dividir por cualquier espacio en blanco
  return words.length <= 150;
}

function isValidJpg(file) {
  const extension = file.name.split(".").pop().toLowerCase();
  const validExtension = extension === "jpg";
  const validSize = file.size <= 100 * 1024; // 100 KB
  return validExtension && validSize;
}

function isValidWebp(file) {
  const extension = file.name.split(".").pop().toLowerCase();
  const validExtension = extension === "webp";
  const validSize = file.size <= 100 * 1024; // 100 KB
  return validExtension && validSize;
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
  }
}

function validateFormRegister() {
  clearErrors();
  const form = document.querySelector(".formCreatedBlog");
  let isValid = true;

  form.querySelectorAll("input, textarea").forEach((input) => {
    const fieldName = input.name;
    const fieldValue = input.value.trim();

    if (fieldName === "title") {
      if (!fieldValue) {
        isValid = false;
        showFieldError(fieldName, "El campo de título es obligatorio");
      } else if (!isValidContentTitle(fieldValue)) {
        isValid = false;
        showFieldError(
          fieldName, "El título no puede tener más de 10 palabras."
        );
      }
    }

    if (fieldName === "descripcion") {
      if (!fieldValue) {
        isValid = false;
        showFieldError(fieldName, "El campo de descripción es obligatorio");
      } else if (!isValidContentDescription(fieldValue)) {
        isValid = false;
        showFieldError(
          fieldName, "El contenido no puede tener más de 22 palabras."
        );
      }
    }

    if (fieldName === "contenido") {
      if (!fieldValue) {
        isValid = false;
        showFieldError(fieldName, "El campo de contenido es obligatorio");
      } else if (!isValidContent(fieldValue)) {
        isValid = false;
        showFieldError(
          fieldName, "El contenido no puede tener más de 150 palabras."
        );
      }
    }

    if (fieldName === "img_jpg") {
      const imgJpgFile = input.files[0];
      if (!imgJpgFile) {
        isValid = false;
        showFieldError(fieldName, "La imagen jpg es obligatoria");
      } else if (!isValidJpg(imgJpgFile)) {
        isValid = false;
        showFieldError(fieldName, "La imagen JPG debe tener extensión .jpg y ser menor de 100 KB"
        );
      }
    }

    if (fieldName === "img_webp") {
      const imgWebpFile = input.files[0];
      if (imgWebpFile && !isValidWebp(imgWebpFile)) {
        isValid = false;
        showFieldError(fieldName, "La imagen WEBP debe tener extensión .webp y ser menor de 100 KB"
        );
      }
    }
  });

  return isValid;
}

// Solicitud fetch a un endpoint 
function checkUserBlog(callback) {
  fetch("/blog/check_user_createBlog")
    .then((response) => response.json())
    .then((data) => {
      callback(data.has_blog);
    })
    .catch((error) => {
      console.error("Error:", error);
      callback(false);
    });
}

/*=============== ENVÍO DE FORMULARIO ===============*/
function submitFormCreatedBlog(event)  {
  event.preventDefault();

  checkUserBlog((hasBlog) => {
    if (hasBlog) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: "Ya has escrito un blog.",
      });
    } else {
      if (validateFormRegister()) {
        const form = document.querySelector(".formCreatedBlog");

        Swal.fire({
          icon: "success",
          title: "¡Formulario válido!",
          text: "Enviando reseña...",
          showConfirmButton: false,
          timer: 1500,
        }).then(() => {
          form.submit();
        });
      } else {
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "Por favor, corrige los errores en el formulario antes de enviarlo.",
        });
        console.log("Formulario inválido. No se puede enviar.");
      }
    }
  });
}