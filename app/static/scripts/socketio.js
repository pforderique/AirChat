document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('/');//'http://' + document.domain + ':' + location.port);
    
    let room = current_room; // auto join this room
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

    // Send Message Button =  Standard event listenter for the click of the button
    document.querySelector('#send_message').onclick = () => {
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

                // change header 
                var chat_header = document.querySelector('#chat-header-title')
                chat_header.innerHTML = `Chat Room: ${room}`;
                // - add leave button IFF its not for the Global chat
                if(room != "Global"){
                    if(!document.contains(document.querySelector(".leave-chat"))){
                        const btn = document.createElement('button');
                        btn.className = "leave-chat btn-danger"
                        const i = document.createElement('i');
                        i.className = "fa fa-times-circle";
                        btn.innerHTML = "Leave " + i.outerHTML; 
                        btn.onclick = () => {
                            // send POST request to /delete-room
                            var xhr = new XMLHttpRequest();
                            xhr.open("POST", `/delete-room`, false);
                            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                            xhr.send(`username=${username}&room_name=${room}`);

                            location.reload();
                            
                            // switch into Global after deleting the room
                            // document.querySelector('#Global').click(); // RIGHT NOW IT JUST PUTS YOU BACK INTO GLOBAL 
                        }
                        chat_header.parentNode.insertBefore(btn, chat_header.nextSibling);

                        // add event listener to it
                        // function delete_room(username, room_name){
                        //     var xmlHttp = new XMLHttpRequest();
                        //     xmlHttp.open( "GET", '/delete-room', false ); // false for synchronous request
                        //     xmlHttp.send( null );
                        //     return xmlHttp.responseText;
                        // }
                        // document.querySelector('.leave-chat').onclick = function() {
                        //     delete_room(username, room)
                        // }

                    }
                } else { 
                    // we are in global -- remove the LEAVE CHAT button if exists
                    if (document.contains(document.querySelector(".leave-chat"))) {
                        document.querySelector(".leave-chat").remove();
                    }
                }
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

// $(document).ready(function() {  
//     var socket = io.connect('/'); //'http://' + document.domain + ':' + location.port);
//     let room = "Global"; // auto join this room
//     joinRoom(room)

//     // message event for the client (message in flask is the backend stuff of course) for when we receive
//     socket.on('message', data =>{
//         var $p = $("<p>");
//         const $span_username = $("<span>");
//         const $span_timestamp = $("<span>");
//         const $br = $("<br>");

//         if (data.username) {
//             // Then this message was sent by a USER
//             $span_username.html(data.username);
//             $span_timestamp.html(data.time_stamp);
//             $p.html($span_username.prop("outerHTML") + $br.prop("outerHTML") + data.msg + $br.prop("outerHTML") + $span_timestamp.prop("outerHTML")); // msg contains the message, as we defined

//             // attach append the data to the end there
//             $('#display-message-section').append($p);
//             // erase the value in the message bar
//             $('#user_message').value = '';
//         } else {
//             // ELSE this was a system generated message
//             printSysMsg(data['msg']);
//         }
//     })
//     // Send Message Button =  Standard event listenter for the click of the button
//     $('#send_message').onclick = () => {
//         // grab the text and send it to the server as a JSON 
//         socket.send({
//             'msg' : document.querySelector('#user_message').value,
//             'username': username, // which we added as a const in our html file
//             'room' : room,
//         } );
//     }

//     // Room Selection
//     $('.select-room').forEach(p => {
//         p.onclick = () => {
//             let newRoom = p.html();
//             if (newRoom === room) {
//                 msg = `You are already in room ${room}.`
//                 printSysMsg(msg);
//             } else {
//                 leaveRoom(room);
//                 joinRoom(newRoom);
//                 room = newRoom;
//             }
//         };  
//     })

//     // Leave room
//     function leaveRoom(room) {
//         socket.emit('leave', {'username': username, 'room' : room });
//     }

//     // Join room
//     function joinRoom(room) {
//         socket.emit('join', {'username': username, 'room' : room });
//         // Clear message area
//         $('#display-message-section').html('');
//         // Autofocus on text box
//         $('#user_message').focus();
//     }
    
//     // Print system message
//     function printSysMsg(msg) {
//         var $p = $("<p>");
//         $p.html(msg);
//         $('#display-message-section').append($p);
//     }
// });  