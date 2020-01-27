var SOCKET_WRITE_DELAY = 100;

var ctrlSocket = new WebSocket('ws://' + window.location.host + '/ws/ctrl/');

ctrlSocket.onmessage = function(data) {
    var message = data['message'];
    // TODO:  Handle message from socket
};

ctrlSocket.onclose = function(data) {
    console.error('Socket closed unexpectedly');
};

/*
ctrlSocket.send(JSON.stringify({
    'message': message
}));
*/

function getTravelSpeed(){
    return $("#jogSpeedRange").val();
}

// Winch Control Buttons
var timeoutId = 0;
function handleWinchCtrlButton(event){
    
    var speed = String($("#jogSpeedRange").val());
    var cmdString = "";
    switch(event.target.id){
        case "winchUp":
            // Jog Up Speed *    
            cmdString = "JUS" + speed;
            break;
        case "winchDown":
            // Jog Down Speed *
            cmdString = "JDS" + speed;
            break;
        default:
            alert("Functionality not yet supported");
            break;
    }
    console.log(cmdString);
    ctrlSocket.send(cmdString);

    
    timeoutId = setTimeout(handleWinchCtrlButton, 100, event);
}
$(document).ready(function() {
    // Handle winch ctrl buttons
    $('.winchCtrl').on('mousedown', function(event) {
        handleWinchCtrlButton(event);
    }).on('mouseup mouseleave', function() {
        clearTimeout(timeoutId);
    });
});