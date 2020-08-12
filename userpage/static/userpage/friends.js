// $(".messages").animate({
//     scrollTop: $(document).height()
// }, "fast");


// function newMessage() {
//     message = $(".message-input input").val();
//     if ($.trim(message) == '') {
//         return false;
//     }
//     $('<li class="sent"><img src="http://emilcarlsson.se/assets/mikeross.png" alt="" /><p>' + message +
//         '</p></li>').appendTo($('.messages ul'));
//     $('.message-input input').val(null);
//     $('.contact.active .preview').html('<span>You: </span>' + message);
//     $(".messages").animate({
//         scrollTop: $(document).height()
//     }, "fast");
// };

// $('.submit').click(function () {
//     newMessage();
// });

// $(window).on('keydown', function (e) {
//     if (e.which == 13) {
//         newMessage();
//         return false;
//     }
// });
// //# sourceURL=pen.js
// function getMessages() {
//     $.get("/userpage/friends/", function (chat_messages) {
//         $('#chatMessages').html(chat_messages);
//         var objDiv = document.getElementById("chatMessagesContainer");
//         objDiv.scrollTop = objDiv.scrollHeight;
//         console.log(chat_messages)
//     });
// }
// setInterval(function () {
//     getMessages()
// }, 3000);

function getMessages() {
    $.get("/userpage/friends/", function(chat_messages){
        let parsedChatMessages = $.parseHTML(chat_messages)
        console.log(parsedChatMessages[25])
    })
}
getMessages()