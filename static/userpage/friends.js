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
        } else if ($(this).html() == 'Members'){
            $('#addMemberSettings').hide()
            $('#groupMembersSettings').show();
        }
    })
    $('#deleteGroup').click(function(evet){
        event.preventDefault();
        let currChat = $('#currChat').attr('data-pk')
        let confirmation = confirm('Are you sure you want to delete the group?')
        if (confirmation){
            $.ajax({
                url: $('#deleteGroup').attr('data-url'),
                data: {
                    'pk': $('#currChat').attr('data-pk'),
                },
                dataType:'json',
                success: function(response){
                    location.reload();
                }
            })
        }
    })
});