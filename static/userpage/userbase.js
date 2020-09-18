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

        // Avatar replacing
        document.querySelector('#div_id_avatar').style.display = 'none'
        let avatarDiv = document.createElement('div')
        let avatarP = document.createElement('p')

        // Style
        avatarDiv.classList.add('form-group')
        avatarP.classList.add('btn')
        avatarP.classList.add('btn-outline-success')

        // Display
        avatarP.innerHTML = '<i class="fas fa-camera-retro"></i> Avatar'
        avatarDiv.append(avatarP)
        document.querySelector('#div_id_avatar').parentElement.append(avatarDiv)
        // Uplading functions
        avatarP.onclick = function (e) {
            e.preventDefault();
            document.querySelector('#id_avatar').click();
        }
        document.querySelector('#id_avatar').onchange = function (e) {
            avatarP.innerHTML = '<i class="fas fa-camera-retro"></i>' + $('#id_avatar')[0].files[0].name
        }


        // Cover replacing
        document.querySelector('#div_id_cover').style.display = 'none'
        let coverDiv = document.createElement('div')
        let coverP = document.createElement('p')

        // Style
        coverDiv.classList.add('form-group')
        coverP.classList.add('btn')
        coverP.classList.add('btn-outline-success')

        // Display
        coverP.innerHTML = '<i class="fas fa-image"></i> Cover'
        coverDiv.append(coverP)
        document.querySelector('#div_id_cover').parentElement.append(coverDiv)
        // Uplading functions
        coverP.onclick = function (e) {
            e.preventDefault();
            document.querySelector('#id_cover').click();
        }
        document.querySelector('#id_cover').onchange = function (e) {
            coverP.innerHTML = '<i class="fas fa-image"></i>' + $('#id_cover')[0].files[0].name
        }

    })
})