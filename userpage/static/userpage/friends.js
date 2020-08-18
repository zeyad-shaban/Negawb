$(document).ready(function () {
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
                url: $('#groupMembersSettings').attr('data-url'),
                data: {
                    'group_id': $('#currChat').attr('data-pk'),
                    'action': 'showMembers'
                },
                dataType: 'json',
                success: function (response) {
                    members = JSON.parse(response.members)
                    for (let i = 0; members.length > i; i++) {
                        $('#groupMembers').prepend(`
                        <li class="list-group-item">
                                <div class="row w-100">
                                    <div class="col-12 col-sm-6 col-md-3 px-0">
                                        <a href="/people/${members[i].pk }">
                                            <img src="/media/profile_images/DefaultUserImage.WebP" alt="${ members[i].fields.username }"
                                            class="img-fluid rounded-circle d-block mx-auto" height="73" width="73">
                                    </a>
                                    </div>
                                    <div class="col-12 col-sm-6 col-md-9 text-center text-sm-left">
                                        <a href="/people/${members[i].pk}/">
                                    <label class="name lead">${ members[i].fields.username }</label>
                                    </a>
                                    <br>
                                    <span class="text-muted" data-toggle="tooltip" title="Bio"
                                    data-original-title="${ members[i].fields.bio }" style="color: black;"></span>
                                    <span class="small text-truncate" style="color: black;">${ members[i].fields.bio }</span>
                                    <form id="id_removeMemberForm${members[i].pk}" method="GET">
                                        <button type="submit" name="invite," data-pk="${members[i].pk}" class="id_removeMember btn float-right"
                                        id="id_removeMember${members[i].pk}"><i class="fas fa-minus-circle"
                                        style="font-size: 36px;"></i></button>
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
                                $.ajax({
                                    url: $('#groupMembersSettings').attr('data-url'),
                                    data: {
                                        'group_id': $('#currChat').attr('data-pk'),
                                        'member_id': member_id,
                                        'action': 'removeMember'
                                    },
                                    method: 'get',
                                    dataType: 'json',
                                    success: function (response) {
                                        $(this).fadeOut()
                                    }
                                })
                            }
                        })
                    }
                    g.text = removeMember()
                    s.parentNode.insertBefore(g, s);
                }
            })
            // List them
            // add kick button beside them ONLY IF ADMIN
            // check if the user going to be kicked is either an admin or author
            // if yes make checker author > admin > member
            // kick or keep (NO RELOAD!!)
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
            // location.reload();
        }
    })
});