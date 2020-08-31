document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        $('#send').click(function (e) {
            e.preventDefault();
            if (!$('#messageInput').val() == '') {
                $.ajax({
                    url: $('#send').attr('data-url'),
                    data: {
                        'action': 'friend',
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