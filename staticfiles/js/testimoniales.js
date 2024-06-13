document.addEventListener("DOMContentLoaded", () => {
  // Enlazar la función submitFormTestimonials al evento de clic del botón de envío
  const submitButton = document.querySelector(".enviar");
  submitButton.addEventListener("click",submitFormTestimonials); /* valida el envio */
});

function clearErrors() {
  const errorMessages = document.querySelectorAll(".error-message");
  errorMessages.forEach((errorMessage) => errorMessage.remove());
}

function isValidContent(content) {
  const words = content.trim().split(/\s+/); // Dividir por cualquier espacio en blanco / palabras 
  return words.length <= 20;
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
  const form = document.querySelector(".formTestimonials");
  let isValid = true;

  form.querySelectorAll("input, textarea").forEach((input) => {
    const fieldName = input.name;
    const fieldValue = input.value.trim();

    if (fieldName === "contenido") {
      if (!fieldValue) {
        isValid = false;
        showFieldError(fieldName, "El campo de reseña es obligatorio");
      } else if (!isValidContent(fieldValue)) {
        isValid = false;
        showFieldError(fieldName, "El contenido no puede tener más de 20 palabras.");
      }
    }
  });

  return isValid;
}

function checkUserTestimonial(callback) {
  fetch("/check_user_testimonial/")
    .then((response) => response.json())
    .then((data) => {
      callback(data.has_testimonial);
    })
    .catch((error) => {
      console.error("Error:", error);
      callback(false);
    });
}

/*=============== ENVÍO DE FORMULARIO ===============*/
function submitFormTestimonials(event) {
    event.preventDefault();
    
    checkUserTestimonial(hasTestimonial => {
        if (hasTestimonial) {
            Swal.fire({
                icon: "error",
                title: "Error",
                text: "Ya has escrito una reseña.",
            });
        } else {
            if (validateFormRegister()) {
                const form = document.querySelector(".formTestimonials");

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
