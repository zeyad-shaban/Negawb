$(document).ready(function () {

    $('.todoNote').css('display', 'none')
    $('.todoItem').on('click', function (event) {
        // $('.todoNote').toggle()
        $('.todoNote', this).toggle()
    })

    // * Load notifications
    setInterval(() => {
        let currNotificationsCount
        if ($('#currNotificationsCount').html()) {
            currNotificationsCount = $('#currNotificationsCount').html()
        } else {
            currNotificationsCount = 0
        }
        $.ajax({
            url: $('#notificationsList').attr('data-url'),
            data: {},
            dataType: 'json',
            success: function (response) {
                let notifications = JSON.parse(response.notifications)
                let newNotificationsCount = notifications.length
                let output = ''
                if (newNotificationsCount != currNotificationsCount) {
                    for (notification of notifications) {
                        output += notification.fields.content
                        output += '<br>'
                    }
                    $('#notificationsList').html(output)
                    $('#currNotificationsCount').html(newNotificationsCount)
                    let notificationAudio = document.getElementById('notificationSound');
                    notificationAudio.play()
                }
            }
        })
    }, 6000);

});