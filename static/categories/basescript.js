$('.todoNote').css('display', 'none')
$('.todoItem').on('click', function (event) {
    // $('.todoNote').toggle()
    $('.todoNote', this).toggle()
})
