let send = document.getElementsByClassName("send");

let message = document.getElementById("id_message");
// let input = document.querySelector('input[type="file"]');
let chat_id = document.querySelector("#requests_pk");

const proto = window.location.protocol === "https:" ? "wss" : "ws";
var chatId = window.location.pathname.split('/')[2];
var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/request/' + chatId + '/'
);

chatSocket.onmessage = (e) =>{
    // var data = JSON.parse(e.data);
    // var messageContent = data['content'];
    // // var messageImage = data['image'];
    // var username = data['username'];

    // var chatContainer = document.querySelector('#chat-container');
    // chatContainer.appendChild(messageElement);
    // chatContainer.appendChild(imageElement);
    console.log(e)
};

function sendMessage(e) {
    let messageInput = document.querySelector("#id_message").value;
    let messageFileInput = document.querySelector('input[type="file"]');
    let messageImage = messageFileInput.files.length > 0 ? messageFileInput.files[0] : null;

    if (messageImage) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var message = {
                'content': messageInput,
                'image': e.target.result ? e.target.result : null,
            };
            chatSocket.send(JSON.stringify(message))
            document.querySelector("#id_message").value = ''
            messageFileInput.value = '';
        };
        reader.readAsDataURL(messageImage);
    } else {
        var message = {
            'content': messageInput,
            'image': null,
        };
        chatSocket.send(JSON.stringify(message));
        document.querySelector("#id_message").value = ''
        messageFileInput.value = '';
    }
}