document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('/');//'http://' + document.domain + ':' + location.port);
    
    let room = "Lounge"; // auto join this room
    joinRoom(room)

    // socket.on('connect', function() { // can also just use () => here too 
    //     socket.send("I am connected!") // using SEND will automatically send it to bucket labeled 'message'
    // });

    // message event for the client (message in flask is the backend stuff of course) for when we receive
    socket.on('message', data =>{
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        if (data.username) {
            // Then this message was sent by a USER
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML; // msg contains the message, as we defined

            // attach append the data to the end there
            document.querySelector('#display-message-section').append(p);
            // erase the value in the message bar
            document.querySelector('#user_message').value = '';
        } else {
            // ELSE this was a system generated message
            printSysMsg(data['msg']);
        }
    })

    // socket.on('some-event', data =>{
    //     console.log(`Message received: ${data}`);
    // })

    // Send Message Button =  Standard event listenter for the click of the button
    document.querySelector('#send_message').onclick = () =>{
        // grab the text and send it to the server as a JSON 
        socket.send({
            'msg' : document.querySelector('#user_message').value,
            'username': username, // which we added as a const in our html file
            'room' : room,
        } );
    };

    // Room Selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom === room) {
                msg = `You are already in room ${room}.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        };
    });

    // Leave room
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room' : room });
    }

    // Join room
    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room' : room });
        // Clear message area
        document.querySelector('#display-message-section').innerHTML = '';
        // Autofocus on text box
        document.querySelector('#user_message').focus();
    }
    
    // Print system message
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }
})