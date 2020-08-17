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
            data: {
                'current_notifications_count': currNotificationsCount
            },
            dataType: 'json',
            success: function (response) {
                let notifications = JSON.parse(response.notifications)
                let newNotificationsCount = notifications.length
                let output = ''
                console.log(newNotificationsCount)
                console.log(currNotificationsCount)
                console.log(notifications)
                if (newNotificationsCount > currNotificationsCount) {
                    for (notification of notifications) {
                        let senderAvatar
                        if (notification.fields.sender.who_see_avatar == 'everyone') {
                            senderAvatar = notification.fields.sender.avatar.url
                        } else {
                            senderAvatar = "/media/profile_images/DefaultUserImage.WebP"
                        }
                        output += `<a href="${ notification.fields.url }" style="text-decoration: none; color: black">
                        <div class="media" style="background: #F7F7F7;">
                            <img src="${senderAvatar}" alt="User Image" width="50" height="64">
                            <div class="media-body">
                                <h5 class="mt-0">${ notification.fields.sender }</h5>
                                <p>${ notification.fields.content }</p>
                            </div>
                        </div>
                    </a>
                    <hr>
                        `
                    }
                    $('#notificationsContainer').prepend(output)
                    $('#currNotificationsCount').html(newNotificationsCount)
                    document.getElementById('notificationSound').play()
                }
            }
        })
    }, 6000);
    $('#notificationDropMenu').click(function (event) {
        event.stopPropagation();
    });

});