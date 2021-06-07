$(document).ready(function() {  

    // Make sidebar collapse on click
    $("#show-sidebar-button").onclick = () => {
        $('#sidebar').classList.toggle('view-sidebar');
    }

    // Makes the 'enter' key submit the message
    $('#user_message').keypress(function (e) {
        var key = e.which;
        if(key == 13){  // the enter key code
           $('#send_message').click();
           return false;  
        }
    });  
});  

