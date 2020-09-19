document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        setInterval(() => {
            if ($('#message_area').html()) {
                setTimeout(() => {
                    $('#message_area').html('')
                }, 4000);
            }
        }, 4000);
    });
});