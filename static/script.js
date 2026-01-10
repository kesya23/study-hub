const socket = io();

function addMessage(user, text, type) {
    const box = document.getElementById("chat-box");
    const msg = document.createElement("div");

    msg.className = "message " + (user === username ? "me" : "other");

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerHTML = `<b>${user}</b><br>${text}`;

    msg.appendChild(bubble);
    box.appendChild(msg);
    box.scrollTop = box.scrollHeight;
}

socket.on("receive_message", data => {
    addMessage(data.username, data.message, data.type);
});

function send() {
    const input = document.getElementById("msg");
    if (!input.value) return;

    socket.emit("send_message", {
        username: username,
        message: input.value
    });

    input.value = "";
}
