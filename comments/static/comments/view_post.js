$(document).ready(function () {
    $('#commentCancelButtons').css('display', 'none')
    $('#commentInput').keyup(() => $('#commentCancelButtons').css('display', 'inline-block'))
    $('#cancelCommentButton').click((e) => {
        e.preventDefault();
        $('#commentCancelButtons').css('display', 'none')
        $('#commentInput').val('')
    })
})