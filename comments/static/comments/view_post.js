document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        $('#editPost').click(function (e) {
            e.preventDefault()
            alert('edit')
        })
        $('#deletePost').click(function (e) {
            e.preventDefault();
            confirmation = confirm('Permanently delete post?')
            if (confirmation) {
                $.ajax({
                    type: "get",
                    url: $('#deletePost').attr('href'),
                    data: {},
                    dataType: "json",
                    async: false,
                    success: function (response) {

                    }
                });
                window.location.replace("https://www.dfreemedia.com/");
            }
        })
        // Like
        $('.likeForm').submit(function (e) {
            e.preventDefault();
            let thisElement = $(this)
            $.ajax({
                url: thisElement.attr('action'),
                data: {
                    'submit': 'like',
                },
                dataType: 'json',
                method: 'get',
                async: false, // Have a look into this
                success: function (response) {
                    let likes = $(`#id_likes${thisElement.attr('data-pk')}`).find('p').html()
                    let dislikes = $(`#id_dislikes${thisElement.attr('data-pk')}`).find('p').html()
                    if (response.action == 'undislike_and_like') {
                        dislikes -= 1
                        likes++
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:black;">${dislikes}</p>`)
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;">${likes}</p>`)
                        // Followed
                        $(`#followed_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:black;">${dislikes}</p>`)
                        $(`#followed_likes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;">${likes}</p>`)
                    } else if (response.action == 'unlike') {
                        likes -= 1
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:black;">${likes}</p>`)
                        // Followed
                        $(`#followed_likes${thisElement.attr('data-pk')}`).html(`<p style="color:black;">${likes}</p>`)
                    } else { //Like only
                        likes++
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;">${likes}</p>`)
                        // Followed
                        $(`#followed_likes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;">${likes}</p>`)
                    }
                }
            })
        })
        // Dislike
        $('.dislikeForm').submit(function (e) {
            e.preventDefault();
            let thisElement = $(this)
            $.ajax({
                url: thisElement.attr('action'),
                data: {
                    'submit': 'dislike',
                },
                dataType: 'json',
                method: 'get',
                async: false,
                success: function (response) {
                    let likes = $(`#id_likes${thisElement.attr('data-pk')}`).find('p').html()
                    let dislikes = $(`#id_dislikes${thisElement.attr('data-pk')}`).find('p').html()
                    if (response.action == 'unlike_and_dislike') {
                        dislikes++
                        likes -= 1
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;">${dislikes}</p>`)
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:black;">${likes}</p>`)
                        // Followed
                        $(`#followed_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;">${dislikes}</p>`)
                        $(`#followed_likes${thisElement.attr('data-pk')}`).html(`<p style="color:black;">${likes}</p>`)
                    } else if (response.action === 'undislike') {
                        dislikes -= 1
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:black;">${dislikes}</p>`)
                        // Followed
                        $(`#followed_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:black;">${dislikes}</p>`)
                    } else {
                        dislikes++
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;">${dislikes}</p>`)
                        // Followed
                        $(`#followed_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;">${dislikes}</p>`)
                    }
                }
            })
        })
    })
})