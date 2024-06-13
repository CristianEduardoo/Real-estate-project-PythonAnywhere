$(function () {
    console.log(user, room_id); // From room.html
  
    /* === Ruta para el web socket == */
    let url = "ws://" + window.location.host + "/ws/chat/room/" + room_id + "/";
    console.log(url);
    console.log(window.location.host);

    /* === WebSocket === */
    let chatWebSocket = new WebSocket(url);
    console.log(chatWebSocket);

    chatWebSocket.onopen = function (e) {
      console.log("WebSocket abierto");
    };

    chatWebSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      // console.log(data.type);
      if (data.type === "chat_message") {
        const msj = data.message;
        const username = data.username;
        const datetime = data.datetime;

        document.querySelector("#boxMessages").innerHTML +=
          ` <div class="alert alert-success" role="alert">
                ${msj}
                <div>
                    <small class="fst-italic fw-bold">${username}</small>
                    <small class="float-end">${datetime}</small>
                </div>
            </div>
          `;
      } else if (data.type === "user_list") {
        let user_listHTML = "";

        for (const username of data.users) {
          const userClass = username === user ? "list-group-item-success" : "";
          user_listHTML += `<li class="list-group-item ${userClass}">@${username}</li>`;
        }

        document.querySelector("#usersList").innerHTML = user_listHTML;
      }
    };

    chatWebSocket.onclose = function (e) {
      console.log("WebSocket cerrado");
    };

  /*===================== JS =====================*/

  const btnChat = document.querySelector("#btnMessage");
  const inputChat = document.querySelector("#inputMessage");

  /*===================== Eventos =====================*/
  btnChat.addEventListener("click", sendMessage);
  inputChat.addEventListener("keypress", inputPress);

  /*=== keyCode => 13 => Tecla Enter  ===*/
  function inputPress(event) {
    if (event.keyCode === 13) {
      sendMessage();
    }
  }

  /*===================== Funciones =====================*/
  function sendMessage() {
    let message = document.querySelector("#inputMessage");
    // console.log(message.value.trim());

    // para reiniciar el input
    if (message.value.trim() !== "") {
      loadMessageHTML(message.value.trim());
      // ===> IMPORTANTE!! ===> Enviar mensaje al servidor
        chatWebSocket.send(
          JSON.stringify({
            type: "chat_message",
            message: message.value.trim(),
          })
        );

      console.log(message.value.trim());

      message.value = "";
    }
  }

  /*=== Inserta en el HTML ===*/
  function loadMessageHTML(message) {
    let currentDatetime = new Date();
    let dateObject = new Date(currentDatetime);

    let year = dateObject.getFullYear();
    let month = ("0" + (dateObject.getMonth() + 1)).slice(-2);
    let day = ("0" + dateObject.getDate()).slice(-2);
    let hours = ("0" + dateObject.getHours()).slice(-2);
    let minutes = ("0" + dateObject.getMinutes()).slice(-2);
    let seconds = ("0" + dateObject.getSeconds()).slice(-2);

    const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    /* === pasamos valores por JS - room.html === */
    document.querySelector("#boxMessages").innerHTML += 
      ` <div class="alert alert-primary" role="alert">
            ${message}
            <div>
                <small class="fst-italic fw-bold">${user}</small>
                <small class="float-end">${formattedDate}</small>
            </div>
        </div>
      `;
  }
});