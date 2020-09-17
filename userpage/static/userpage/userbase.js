document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        // --------------------------------
        // Navigate edit profile
        // --------------------------------
        $('.editForm').hide()
        $('#personalForm').show()
        $('#editNavbar ul li').click(function (e) {
            e.preventDefault()
            $('.editForm').hide()
            if ($(this).html().includes('Personal')) {
                $('#personalForm').show()
            } else if ($(this).html().includes('Distraction Free')) {
                $('#distractionFreeForm').show()
            } else if ($(this).html().includes('Privacy')) {
                $('#privacyForm').show()
            } else {
                $('#advanceForm').show()
            }
        })

        // ---------------
        // Display text
        // ---------------
        $('#id_avatar').change(function () {
            console.log('Changed')
            var i = $(this).prev('label').clone();
            var file = $('#id_avatar')[0].files[0].name;
            $(this).prev('label').text(file);
        });
        $('#id_cover').change(function () {
            console.log('Changed')
            var i = $(this).prev('label').clone();
            var file = $('#id_cover')[0].files[0].name;
            $(this).prev('label').text(file);
        });
    })
})