document.addEventListener('DOMContentLoaded', () => {

    // Make sidebar collapse on click
    document.querySelector('#show-sidebar-button').onclick = () => {
        document.querySelector('#sidebar').classList.toggle('view-sidebar');
    };

    // Makes the 'enter' key submit the message
    let msg =  document.querySelector('#user_message');
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        // key code 13 is the ENTER key
        if(event.keyCode === 13){
            document.querySelector('#send_message').click();
        }
    })
    
})