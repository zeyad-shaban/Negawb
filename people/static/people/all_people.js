document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        // * Add Friend Button
        $('.addFriend').click(function (e) {
            e.preventDefault();
            let thisElement = $(this)
            $.ajax({
                url: thisElement.attr('href'),
                data: {},
                dataType: 'json',
                success: function (response) {
                    thisElement.parent().fadeOut()
                    $('#message_area').html('')
                    if (response.message.tags === 'error') {
                        $('#message_area').append(`
                            <div class="alert alert-danger fixed-top">${response.message.text}</div>
                            `)
                    } else {
                        $('#message_area').append(`
        <div class="alert alert-${response.message.tags} fixed-top">${response.message.text}</div>
                                `)
                    }
                    thisElement.fadeOut()
                }
            })
        })

        // Bottom scroll
        let i = 2;

        function bottomScroll(event) {
            if ($(window).scrollTop() + $(window).height() == $(document).height()) {
                $.ajax({
                    url: window.location.pathname,
                    data: {
                        'page': i
                    },
                    method: 'get',
                    dataType: 'json',
                    async: false,
                    success: function (response) {
                        i++
                        users = JSON.parse(response.users)
                        for (user of users) {
                            let userAvatar
                            let userPhoneNum = ''
                            if (user.fields.who_see_avatar == 'everyone') {
                                userAvatar =
                                    `<img src="/media/${user.fields.avatar}" alt="{{ view_user.username }}"
                            class="img-fluid rounded-circle d-block mx-auto" height="73" width="73">`
                            } else if (user.fields.who_see_avatar == 'friends' &&
                                "{{user}}" in user
                                .fields.friends) {
                                userAvatar =
                                    `<img src="/media/${user.fields.avatar}" alt="${user.fields.username}"
                            class="img-fluid rounded-circle d-block mx-auto" height="73" width="73">`
                            } else {
                                userAvatar =
                                    `<img src="/media/profile_images/DefaultUserImage.jpg" alt="${user.fields.username}"
                                class="img-fluid rounded-circle d-block mx-auto" height="73" width="73">`
                            }
                            if (user.fields.phone) {
                                userPhoneNum = `<span class="fa fa-fw fa-phone fa-fw text-muted" data-toggle="tooltip" title="Phone Number"
                        data-original-title="${ user.fields.phone }"></span>
                    <span class="text-muted small">${ user.fields.phone }</span>
                    <br>`
                            }
                            output = `
                    <li class="">
                    <div class="row w-100">
                    <div class="userInfo">
                        <a href="/people/${user.pk}">
                        ${userAvatar}
                    </a>
                    </div>
                    <a href="/people/${user.pk}">
                        <label class="name lead">${user.fields.username}</label>
                        </a>
                        <br>
                        
                        <div class="userDesc">
                            ${userPhoneNum}
                            <span class="small text-truncate">${ user.fields.bio }</span>
                            <form action="/people/addfriend/${user.pk}" method="GET" id="idAddFriendForm">
                                <a href="/people/add_friend/${user.pk}" class="btn addFriend"><i
                    class="fas fa-user-plus"></i> Add friend</a>
                            </form>
                        </div>
                    </div>
                    </li>
                        `
                            $('#contact-list').append(output)
                        }
                        var g = document.createElement('script')

                        function addFriend() {
                            $('.addFriend').click(function (e) {
                                e.preventDefault();
                                let thisElement = $(this)
                                $.ajax({
                                    url: thisElement.attr('href'),
                                    data: {},
                                    dataType: 'json',
                                    success: function (response) {
                                        thisElement.parent().fadeOut()
                                        $('#message_area').html('')
                                        if (response.message.tags === 'error') {
                                            $('#message_area').append(`
                                                <div class="alert alert-danger fixed-top">${response.message.text}</div>
                                                `)
                                        } else {
                                            $('#message_area').append(`
                            <div class="alert alert-${response.message.tags} fixed-top">${response.message.text}</div>
                                                    `)
                                        }
                                        thisElement.fadeOut()
                                    }
                                })
                            })
                        }
                        var s = document.getElementsByName('script')[0]
                        g.text = addFriend();
                        s.parentNode.insertBefore(g, s)
                    }
                })
            }
        }
        bottomScroll()
        $(window).scroll(function () {
            bottomScroll()
        });

    });
});