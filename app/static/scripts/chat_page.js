$(document).ready(function() {  

    // Make sidebar collapse on click
    $("#show-sidebar-button").click(function() {
        $('#sidebar').classList.toggle('view-sidebar');
    });

    // Makes the 'enter' key submit the message
    $('#user_message').keypress(function (e) {
        var key = e.which;
        if(key == 13){  // the enter key code
           $('#send_message').click();
           return false;  
        }
    });
    
    /* MODAL LOGIC */
    var $modal = $('#room_modal') // Get the modal
    var $btn = $('#open_modal') // Get the button that opens the modal
    var $span = $('.close') // Get the <span> element that closes the modal

    // When the user clicks on the button, open the modal
    $btn.click(function() { 
        $modal.css("display", "block");
    })
  
    // When the user clicks on <span> (x), close the modal
    $span.click(function() { 
        $modal.css("display", "none");
    })
    
    // // When the user clicks anywhere outside of the modal, close it
    // $(window).click(function(event) {
    //     if (event.target == $modal) {
    //         $modal.css("display", "none");
    //     }
    // })

});  


