$(document).ready(function () {
    $('#addGroupButton').click(function (e) {
        e.preventDefault();
        $('#newGroupForm').submit()
    });
    $('#findUserForm').submit(function (e) {
        e.preventDefault();
    })
    $('nav').removeClass('sticky-top')
});