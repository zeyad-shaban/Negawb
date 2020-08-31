document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        $('#addGroupButton').click(function (e) {
            e.preventDefault();
            $('#newGroupForm').submit()
        });
        $('#findUserForm').submit(function (e) {
            e.preventDefault();
        })
        $('nav').removeClass('sticky-top')
        $('#addMemberSettings').hide()
        $('.groupSettings').click(function (event) {
            event.preventDefault();
            $('.groupSettings').removeClass('active');
            $(this).addClass('active');
            if ($(this).html() == 'Add') {
                $('#groupMembersSettings').hide()
                $('#addMemberSettings').show()
            } else if ($(this).html() == 'Members') {
                $('#addMemberSettings').hide()
                $('#groupMembersSettings').show();
                $('#groupMembers').html('')
                $.ajax({
                    url: $('#groupMembersSettings').attr('data-url'), // social:group_members
                    data: {
                        'group_id': $('#currChat').attr('data-pk'),
                        'action': 'showMembers'
                    },
                    dataType: 'json',
                    success: function (response) {
                        group = response.group
                        members = JSON.parse(response.members)
                        admins = JSON.parse(group.admins)
                        for (let i = 0; members.length > i; i++) {
                            let badge = ''
                            if (members[i].fields.username == group.author_username) {
                                badge = '<i class="fas fa-crown"></i>'
                            } else {
                                for (admin of admins) {
                                    if (admin.fields.username === members[i].fields.username) {
                                        badge = '<i class="fas fa-user-cog"></i>'
                                    }
                                }
                            }
                            // Get group admins
                            $('#groupMembers').prepend(`
                        <li class="list-group-item">
                                <div class="row w-100">
                                    <div class="col-12 col-sm-6 col-md-3 px-0">
                                        <a href="/people/${members[i].pk }">
                                            <img src="/media/profile_images/DefaultUserImage.jpg" alt="${ members[i].fields.username }"
                                            class="img-fluid rounded-circle d-block mx-auto" height="73" width="73">
                                    </a>
                                    </div>
                                    <div class="col-12 col-sm-6 col-md-9 text-center text-sm-left">
                                        <a href="/people/${members[i].pk}/">
                                    <label class="name lead">${ members[i].fields.username } <span class="badge badge-secondary">${badge}</span>
                                    </label> 
                                    </a>
                                    <br>
                                    <span class="text-muted" data-toggle="tooltip" title="Bio"
                                    data-original-title="${ members[i].fields.bio }" style="color: black;"></span>
                                    <span class="small text-truncate" style="color: black;">${ members[i].fields.bio }</span>
                                    <form id="id_removeMemberForm${members[i].pk}" method="GET">
                                        <button type="submit" name="invite," data-pk="${members[i].pk}" class="id_removeMember btn float-right"
                                        id="id_removeMember${members[i].pk}"><i class="fas fa-minus-circle"
                                        style="font-size: 24px;"></i></button>
                                        </form>
                                        </div>
                                        </div>
                                        </li>
                        `)
                        }
                        var g = document.createElement('script');
                        var s = document.getElementsByTagName('script')[0];

                        function removeMember() {
                            $(`.id_removeMember`).click(function (e) {
                                e.preventDefault();
                                let member_id = $(this).attr('data-pk')
                                let confirmation = confirm(`Are you sure you want to remove ${members[member_id-1].fields.username}`)
                                if (confirmation) {
                                    let thisElement = $(this)
                                    $.ajax({
                                        url: $('#groupMembersSettings').attr('data-url'), // social:group_members   
                                        data: {
                                            'group_id': $('#currChat').attr('data-pk'),
                                            'member_id': member_id,
                                            'action': 'removeMember'
                                        },
                                        method: 'get',
                                        dataType: 'json',
                                        success: function (response) {
                                            if (response.message.includes('You cannot remove')) {
                                                alert(response.message)
                                                thisElement.parent().fadeOut()
                                            } else {
                                                thisElement.parent().parent().parent().parent().toggle()
                                            }
                                        }
                                    })
                                }
                            })
                        }
                        g.text = removeMember()
                        s.parentNode.insertBefore(g, s);
                    }
                })
                // make group admin
            }
        })
        $('#deleteGroup').click(function (evet) {
            event.preventDefault();
            let currChat = $('#currChat').attr('data-pk')
            let confirmation = confirm('Are you sure you want to delete the group?')
            if (confirmation) {
                $.ajax({
                    url: $('#deleteGroup').attr('data-url'),
                    data: {
                        'pk': $('#currChat').attr('data-pk'),
                    },
                    dataType: 'json',
                    success: function (response) {
                        location.reload();
                    }
                })
            }
        })
        // Leave Group
        $('#leaveGroup').click(function (e) {
            e.preventDefault();
            let currChat = $('#currChat').attr('data-pk')
            let confirmation = confirm('You are about to leave this group')
            if (confirmation) {
                $.ajax({
                    url: $('#leaveGroup').attr('data-url'),
                    data: {
                        'pk': $('#currChat').attr('data-pk'),
                    },
                    dataType: 'json',
                    success: function (response) {
                        location.reload();
                    }
                })
            }
        })
        $('#sidepanelCollapser').hide();

        $('#sidepanelCollapser').click(function (e) {
            e.preventDefault();
            $('#sidepanel').slideToggle();
        });

        function windowResizing() {
            if ($(window).width() <= 704) {
                $('#sidepanelCollapser').show();
                $('.contact').click(function (e) {
                    e.preventDefault();
                    $('#sidepanel').toggle();
                });
            }
            if ($(window).width() >= 704) {
                $('#sidepanel').show();
                $('#sidepanelCollapser').hide();
                $('.content').show();
            }
        }
        windowResizing()
        $(window).resize(function (event) {
            windowResizing()
        })
        // $('#inputMessage').emojioneArea({
        //     events: {
        //         keyup: function (editor, event) {
        //             var code = (event.keyCode ? event.keyCode : event.which);
        //             if (code == 13) { //Enter keycode
        //                 $('#sendMessageForm').submit()
        //             }
        //         }
        //     }
        // });
        // Load chat
        function loadMessages(action, pk) {
            $.ajax({
                url: $('#chatMessages').attr('data-url'),
                data: {
                    'pk': pk,
                    'action': action,
                },
                dataType: 'json',
                success: function (response) {
                    console.log('Success')
                    let friend_image
                    let isOld
                    if (response.friend.id <= 1000) {
                        isOld = 'oldUser'
                    }
                    if (response.friend.who_see_avatar == 'everyone' ||
                        response.friend.who_see_avatar == 'friends') {
                        friend_image = response.friend.avatar
                    } else {
                        friend_image =
                            '/media/profile_images/DefaultUserImage.jpg'
                    }
                    $('#friendProfile').html(
                        // ! Absolute URL
                        `<a href="/people/${response.friend.id}/">
                                            <img src="${friend_image}" width="40" height="40" class="${isOld}"/>
                                            </a>
                                            <p id="currChat" data-pk="${response.friend.id}" data-action="friend">${response.friend.username}</p>`
                    )
                    $('#chatMessages').html('')
                    let chat_messages = JSON.parse(response
                        .chat_messages)
                    for (message of chat_messages) {
                        let messageStyle = "null"
                        if (message.fields.is_important) {
                            messageStyle =
                                'style="background: #d10c0c; color: white"'
                        }
                        if (message.fields.message_sender == response
                            .friend.id) {
                            $('#chatMessages').append(`<li class="replies">
                                    <img src="${friend_image}" alt="" width="22" height="22" class="${isOld}"/>
                                    <p ${messageStyle}>${message.fields.message}</p>
                                </li>`)
                        } else {
                            $('#chatMessages').append(`
                                            <li class="sent">
                        <img src="" alt="" width="22" height="22" class="{% if user.id <= 1000 %}oldUser{% endif %}"/>
                        <p id="messageContent" data-currMessagesCount="${chat_messages.length}" ${messageStyle}>${message.fields.message}</p>
                    </li>
                                            `)
                        }
                    }
                    paginateMessages();
                }
            })
        }
        $('.chatFriendButton').click(function (e) {
            let thisElement = $(this)
            let pk = thisElement.attr('data-pk')
            if ($('#currChat').attr('data-pk') == pk) {
                return false
            } else {
                loadMessages('friend', pk)
            }
        })

        // load more messages
        let page = 1;
        function paginateMessages(){
            $.ajax({
                url: $('#chatMessages').attr('data-url'),
                data: {
                    'pk': $('#currChat').attr('data-pk'),
                    'action': 'friend',
                    'page': page
                },
                method: 'get',
                dataType: 'json',
                async: false,
                success: function (response) {
                    page++
                    let chat_messages = JSON.parse(response.chat_messages)
                    chat_messages.reverse()
                    if (chat_messages.length > 0) {
                        for (message of chat_messages) {
                            let messageStyle = ""
                            if (message.fields.is_important) {
                                messageStyle =
                                    'style="background: #d10c0c; color: white"'
                            }
                            if (message.fields.message_sender == response
                                .friend.id) {
                                $('#chatMessages').prepend(`<li class="replies">
                <img src="" alt="" width="22" height="22" class=""/>
                <p ${messageStyle}>${message.fields.message}</p>
            </li>`)
                            } else {
                                $('#chatMessages').prepend(`
                        <li class="sent">
    <img src="{{user.avatar.url}}" alt="" width="22" height="22" class="{% if user.id <= 1000 %}oldUser{% endif %}"/>
    <p id="messageContent" data-currMessagesCount="${chat_messages.length}" ${messageStyle}>${message.fields.message}</p>
</li>
                        `)
                            }
                        }
                    }
                }
            })
        }
        let messagesContainer = document.getElementById('chatMessagesContainer')
        $('#chatMessagesContainer').scroll(function(e){
            if (messagesContainer.scrollTop == 0){
                paginateMessages();
            }
        })
    });
});