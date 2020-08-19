$(document).ready(function () {

    $('.homepageItem').hide()
    if ($('.homepageView').eq(0).hasClass('active')) {
        $('#postsContainer').show()
    } else if ($('.homepageView').eq(1).hasClass('active')) {
        console.log('showing categories...')
        $('#categoryContainer').show()
    }
    $('.homepageView').click(function (e) {
        e.preventDefault();
        if (!$(this).hasClass('active')) {
            $('.homepageView').removeClass('active')
            $(this).addClass('active')
            $('.homepageItem').hide()
            if ($(this).html() === 'Categories') {
                $('#categoryContainer').show()
            } else if ($(this).html() === 'Posts') {
                $('#postsContainer').show()
            } else if ($(this).html() == 'Friends Posts') {
                $('#friendsPosts').show()
            } else if ($(this).html() == 'Followed Posts') {
                $('#followedPosts').show()
            }
        }
    })
})