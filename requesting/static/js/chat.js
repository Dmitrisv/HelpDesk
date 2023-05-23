let send = document.getElementsByClassName("send");

let chat_id = document.querySelector("#requests_pk");

const proto = window.location.protocol === "https:" ? "wss" : "ws";
var chatId = window.location.pathname.split('/')[2];
var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/request/' + chatId + '/'
);

chatSocket.onmessage = (e) =>{
    let data = JSON.parse(e.data);
    if (data["type_event"]==="new_chat_message"){
        let messageContent = data['content'];
        let messageImage_thumb = data['image'];
        let messageImage_src = data['image_src'];
        let username = data['username'];
    
        let html = `
        <div class="card-body">
            <h5 class="card-title text-dark mt-3">${username}</h5>
            <p class="card-text text-muted">${messageContent}</p>
    `;
    
        if (messageImage_thumb) {
            html += `
                <div class="img-fluid">
                    <img src="${messageImage_thumb}" id="image" class="rounded border border-primary" alt="" name="${messageImage_src}">
                </div>
            `;
        }
        
        html += `
            </div>
        `;
      
        let chatContainer = document.querySelector('.chat-container');
        chatContainer.insertAdjacentHTML("beforeend", html);
        console.log(e)
    }
};

function sendMessage(e) {
    let messageInput = document.querySelector("#id_message").value;
    let messageFileInput = document.querySelector('input[type="file"]');
    let messageImage = messageFileInput.files.length > 0 ? messageFileInput.files[0] : null;

    if (messageInput != ''){
        if (messageImage) {
            var reader = new FileReader();
            reader.onload = function (e) {
                var message = {
                    'content': messageInput,
                    'image': e.target.result
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
}