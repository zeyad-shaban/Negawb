document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        // Navbar
        $('body').css('padding-top', $('.navbar').outerHeight() + 'px')

        // detect scroll top or down
        if ($('.main-nav').length > 0) { // check if element exists
            var last_scroll_top = 0;
            $(window).on('scroll', function () {
                scroll_top = $(this).scrollTop();
                if (scroll_top < last_scroll_top) {
                    $('.main-nav').removeClass('scrolled-down').addClass('scrolled-up');
                } else {
                    $('.main-nav').removeClass('scrolled-up').addClass('scrolled-down');
                }
                last_scroll_top = scroll_top;
            });
        }
        // Signup msg
        setInterval(() => {
            if ($('#message_area').html()) {
                setTimeout(() => {
                    $('#message_area').html('')
                }, 4000);
            }
        }, 4000);
    });
});