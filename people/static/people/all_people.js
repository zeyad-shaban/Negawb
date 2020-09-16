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
                    thisElement.fadeOut()
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
                document.querySelector('#loading').innerHTML = `<div class="spinner-border text-primary" role="status">
                <span class="sr-only">Loading...</span>
              </div>`
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
                        if (users.length <= 0) {
                            document.querySelector('#loading').innerHTML = ''
                        } else {
                            for (user of users) {
                                let userAvatar
                                let userPhoneNum = ''
                                let userEmail = ''
                                if (user.fields.show_email) {
                                    userEmail = `
                                <span class="fa fa-fw fa-envelope fa-fw"></span>
                                <span class="small text-truncate">${user.fields.email}</span>
                                <br style="margin-bottom: 10px">
                                `
                                }
                                if (user.fields.who_see_avatar == 'everyone') {
                                    userAvatar =
                                        `<img src="/media/${user.fields.avatar}" alt="X"
                            class="img-fluid rounded-circle d-block mx-auto" height="73" width="73">`
                                } else if (user.fields.who_see_avatar == 'friends' && $('#Userusername').attr('data-username') in user
                                    .fields.friends) {
                                    userAvatar =
                                        `<img src="/media/${user.fields.avatar}" alt="X"
                            class="img-fluid rounded-circle d-block mx-auto" height="73" width="73">`
                                } else {
                                    userAvatar =
                                        `<img src="/media/profile_images/DefaultUserImage.jpg" alt="X"
                                class="img-fluid rounded-circle d-block mx-auto" height="73" width="73">`
                                }
                                if (user.fields.phone) {
                                    userPhoneNum = `<span class="fa fa-fw fa-phone fa-fw text-muted" data-toggle="tooltip" title="Phone Number"
                        data-original-title="${ user.fields.phone }"></span>
                    <span class="text-muted small">${ user.fields.phone }</span>
                <br style="margin-bottom: 10px">
                `
                                }
                                output = `
                    <li class="">
                    <div class="row w-100">
                    <div class="userInfo">
                    <a href="/people/${user.pk}">
                    ${userAvatar}
                    </a>
                    </div>
                    <div class="userDesc">
                    <a href="/people/${user.pk}" class="btn" style="font-size: 150%; font-weight: 300;">
                    <span style="margin-bottom: 10px; display: inline-block">${user.fields.username}</span>
                </a>
                <br>
                    ${userPhoneNum}
                ${userEmail}

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
                                            thisElement.fadeOut()
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
                            let s = document.getElementsByName('script')[0]
                            g.text = addFriend();
                            s.parentNode.insertBefore(g, s)
                        }
                    }
                })
            }
        }
        bottomScroll()
        window.onscroll = function () {
            bottomScroll()
        };

    });
});