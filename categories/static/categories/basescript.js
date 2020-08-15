$(document).ready(function () {

    $('.todoNote').css('display', 'none')
    $('.todoItem').on('click', function (event) {
        // $('.todoNote').toggle()
        $('.todoNote', this).toggle()
    })

    // * Load notifications
    setInterval(() => {
        $.ajax({
            url: $('#notificationsList').attr('data-url'),
            data: {

            },
            dataType: 'json',
            success: function (response) {

            }
        })
    }, 6000);
});