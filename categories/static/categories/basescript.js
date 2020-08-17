$(document).ready(function () {
    var notificationOutput = ''
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
    $('.notificationType').click(function (e) {
        e.preventDefault();
        $('.notificationType').removeClass('active');
        $(this).addClass('active')
        let wantedType = $(this).attr('date-wantedType')
        $.ajax({
            url: $('#notificationsList').attr('data-url'),
            data: {
                'notification_type': wantedType,
            },
            dataType: 'json',
            method: 'get',
            success: function (response) {
                notifications = JSON.parse(response.notifications)
                    for (notification of notifications) {
                        $.ajax({
                            url: $('#notificationsList').attr('data-getUserUrl'),
                            data: {
                                'pk': notification.fields.sender
                            },
                            dataType: 'json',
                            method: 'get',
                            success: function (response) {
                                let sender = response.user
                                sender_friends = JSON.parse(sender.friends)
                                let currUser = $('#notificationsList').attr('data-currUser')
                                let senderAvatar
                                if (sender.who_see_avatar == 'everyone') {
                                    senderAvatar = sender.avatar
                                    // } else if (sender.who_see_avatar == 'friends' && currUser in sender_friends) {
                                    //     console.log('iam in his friends!')
                                } else {
                                    senderAvatar = '/media/profile_images/DefaultUserImage.WebP'
                                }
                                notificationOutput += `
                                <a href="${notification.fields.url}" style="text-decoration: none; color: black">
                                    <div class="media" style="background: #F7F7F7;">
                                        <img src="${sender.avatar}" alt="User Image" width="50"
                                            height="50">
                                        <div class="media-body">
                                            <h5 class="mt-0">${ sender.username }</h5>
                                            <p>${ notification.fields.content }</p>
                                        </div>
                                    </div>
                                </a>
                                <hr>
                                `
                            }
                        })
                }
                $('#notificationsContainer').html(notificationOutput)
                notificationOutput = ''
            }
        })
    });
});