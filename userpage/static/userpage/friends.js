$(document).ready(function () {
    $('#addGroupButton').click(function (e) {
        e.preventDefault();
        $('#newGroupForm').submit()
    });
    $('#findUserForm').submit(function (e) {
        e.preventDefault();
    })
    $('.id_inviteForm').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: $('.id_inviteForm').attr('data-url'),
            data: {
                'user_pk': $(this).attr('data-user_pk'),
                'group_pk': $('#currChat').attr(
                    'data-pk'),
            },
            dataType: 'json',
            success: function (response) {
                console.log('success')
                $('.id_inviteForm', this).fadeOut();
            }
        })
    });
});