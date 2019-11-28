var ctrlSocket = new WebSocket('ws://' + window.location.host + '/ws/ctrl/');

ctrlSocket.onmessage = function(data) {
    var message = data['message'];
    // TODO:  Handle message from socket
};

ctrlSocket.onclose = function(data) {
    console.error('Chat socket closed unexpectedly');
};

/*
ctrlSocket.send(JSON.stringify({
    'message': message
}));
*/
