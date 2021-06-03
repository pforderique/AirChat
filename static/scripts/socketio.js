document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // socket.on('connect', function() { // can also just use () => here too 
    //     socket.send("I am connected!") // using SEND will automatically send it to bucket labeled 'message'
    // });

    // message event for the client (message in flask is the backend stuff of course) for when we receive
    socket.on('message', data =>{
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        span_username.innerHTML = data.username;
        span_timestamp.innerHTML = data.time_stamp;
        p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML; // msg contains the message, as we defined

        // attach append the data to the end there
        document.querySelector('#display-message-section').append(p);
        // erase the value in the message bar
        document.querySelector('#user_message').value = '';
    })

    // socket.on('some-event', data =>{
    //     console.log(`Message received: ${data}`);
    // })

    // Send Message Button =  Standard event listenter for the click of the button
    document.querySelector('#send_message').onclick = () =>{
        // grab the text and send it to the server as a JSON 
        socket.send({
            'msg' : document.querySelector('#user_message').value,
            'username': username // which we added as a const in our html file
        } );
    }
})