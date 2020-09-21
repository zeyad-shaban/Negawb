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

        // Feedback
        $('#send_feedback').click(function (e) {
            e.preventDefault();

            function replaceFeedbackForm() {
                $('#feedback-form').html(`
                <div style="text-align: center;">
                    <i class="far fa-check-circle" style="font-size: 150px; color: green; margin-bottom: 30px;"></i>
                    <br>
                    <p style="font-size: 130%;">Thank you for your time</p>
                    <p style="font-size: 130%;">Your feedback is <b>very valuable</b> to us!</p>
                    <br>
                    <p>You can see your feedback <a href="/feedback">here</a></p>
                </div>
                        `)
            }
            if ($('#feedback_review').val() && $('#feedback_name').val()) {
                $.ajax({
                    url: $('#feedback-form').attr('action'),
                    data: {
                        csrfmiddlewaretoken: $('#feedback-form').attr('data-csrf_token'),
                        name: $('#feedback_name').val(),
                        review: $('#feedback_review').val(),
                        email: $('#feedback_email').val(),
                    },
                    method: 'post',
                    dataType: 'json',
                    success: response => replaceFeedbackForm(),
                    error: response => replaceFeedbackForm(),
                })
            }
        })

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