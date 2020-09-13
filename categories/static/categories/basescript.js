document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        setInterval(() => {
            if ($('#message_area').html()) {
                setTimeout(() => {
                    $('#message_area').html('')
                }, 4000);
            }
        }, 4000);
        $('.addEmoji').emojioneArea({
            pickerPosition: "bottom",
        })

        // * Load notifications
        setInterval(() => {
            let notifications = document.querySelectorAll('.notification');
            let last_notification = $('.notification').eq(0)
            let last_notification_id = last_notification.attr('data-pk')
            $.ajax({
                url: $('#notificationsList').attr(
                    'data-url'), //url social:load_notifications
                data: {
                    'last_notification_id': last_notification_id,
                },
                dataType: 'json',
                method: 'get',
                success: function (response) {
                    let notifications = JSON.parse(response.notifications)
                    if (notifications.length > 0) {
                        for (notification of notifications) {
                            $.ajax({
                                url: $('#notificationsList').attr('data-getUserUrl'), // 'userpage:get_user_by_id'
                                data: {
                                    pk: notification.fields.sender,
                                },
                                method: 'get',
                                dataType: 'json',
                                success: function (user_response) {
                                    let user = user_response
                                        .user;
                                    $('#notificationsContainer')
                                        .prepend(`
                                        <li style="background-color: #EBF0FF;" class="notification" data-pk="${notification.pk}">
                                            <a href="/social/click_notification/${notification.pk}">
                                                <div class="media">
                                                    <img src="${user.avatar}" class="" alt="" width="50" height="50">
                                                    <div class="media-body">
                                                        <h5 class="mt-0">${user.username}</h5>
                                                        <p>${notification.fields.content}</p>
                                                    </div>
                                                </div>
                                            </a>
                                        </li>
                                                `)
                                }
                            })
                        }
                        $('#notificationsCount').html(notifications.length +
                            parseInt($('#notificationsCount').html()))
                        document.querySelector('#notificationSound').play()
                    }
                }
            })
        }, 7000);
        $('#notificationDropMenu').click(function (event) {
            event.stopPropagation();
        });
    });
});