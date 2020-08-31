document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        $('#send').click(function (e) {
            e.preventDefault();
            let messageInput = $('#messageInput').val()
            let is_important = "False"
            if ($('#is_important').is(':checked')) {
                is_important = "True"
            }
            if (!messageInput == '') {
                $.ajax({
                    url: $('#send').attr('data-url'),
                    data: {
                        'action': 'friend',
                        'message': messageInput,
                        'is_important': is_important,
                    },
                    method: 'get',
                    dataType: 'json',
                    success: function (response) {
                        console.log('Success')
                    }
                })
            }
        })
    })
})