document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        let homepage_post_page = 2
        let followed_post_page = 2
        $('.homepageItem').hide()
        $('#postsContainer').show()
        $('.homepageView').click(function (e) {
            e.preventDefault();
            if (!$(this).hasClass('active')) {
                $('.homepageView').removeClass('active')
                $(this).addClass('active')
                $('.homepageItem').hide()
                if ($(this).html() === 'Topics') {
                    $('#categoryContainer').show()
                } else if ($(this).html() === 'Posts') {
                    $('#postsContainer').show()
                } else if ($(this).html() == 'Followed') {
                    $('#followedPosts').show()
                }
            }
        })


        function bottomScroll() {
            if ($(window).scrollTop() + $(window).height() == $(document).height() && $('.homepageView.active').html() == 'Posts') {
                $.ajax({
                    url: '',
                    data: {
                        'homepage_posts_page': homepage_post_page
                    },
                    method: 'get',
                    dataType: 'json',
                    async: false,
                    success: function (response) {
                        homepage_post_page++
                        posts = JSON.parse(response.homepage_posts)
                        for (post of posts) {
                            let output = ''
                            $.ajax({
                                url: $('#categoryContainer').attr('data-url'),
                                data: {
                                    'pk': post.fields.user,
                                },
                                method: 'get',
                                dataType: 'json',
                                async: false,
                                success: function (response) {
                                    let user = response.user
                                    let output = ''
                                    let userAvatar = ''
                                    let isOld = ''
                                    if (user.id <= 1000) {
                                        isOld = 'oldUser'
                                    }
                                    if (user.who_see_avatar == 'everyone') {
                                        userAvatar = user.avatar
                                    } else if (user.who_see_avatar == 'friends' && $('#categoryContainer').attr('data-currUser') in JSON.parse(user.friends)) {
                                        userAvatar = user.avatar
                                    } else if ($('#categoryContainer').attr('data-currUser') == user) {
                                        userAvatar = user.avatar
                                    } else {
                                        userAvatar = `/media/profile_images/DefaultUserImage.jpg`
                                    }
                                    output = `
                                    <a href="/people/${user.id}">
        <img src="${userAvatar}" alt="${user.username }" width="64" height="64"
            class="mr-3 float-left rounded-circle ${isOld}" loading="lazy">
            <span>${user.username}</span>
    </a>
    <div class="mb-3">
        <div class="card-body">
                                    `
                                    if (post.fields.description) {
                                        output += `
                                        <blockquote class="blockquote mb-0">
                <p class="text-break">${post.fields.description}</p>
            </blockquote>
                                    `
                                    }
                                    output += `<small class="form-text text-muted">${post.fields.views.length} Views ♦︎ ${ post.fields.post_date }</small>`
                                    if (post.fields.image) {
                                        output += `<img src="/media/${ post.fields.image }" alt="${ user.username }" height="250" width="40%">                                    `
                                    }
                                    if (post.fields.post_file) {
                                        output += `
                                        <video width="100%" controls class="col-md-10 col-lg-8" preload="none">
                <source src="${ post.fields.post_file }" type="video/mp4">
                <source src="/media/${ post.fields.post_file }" type="video/ogg">
                Your browser does not support the video tag.
            </video>
                                    `
                                    }
                                    output += `
                                    </div>
                                </div>
                                <span class="row justify-content-center">
    <span><a href="/comments/${post.pk}" style="text-decoration: none; color:black;"><i
                class="far fa-comment-dots" style="font-size:36px;"></i></a></span>
    <!-- Like -->
    <form action="/comments/post_like_dislike/${post.pk}/" method="GET" class="form-inline likeForm" data-pk="${post.pk}">
        <button type="submit" name="submit" value="like" title="Like" class="btn btn-link">
            <i class="fa fa-thumbs-o-up" aria-hidden="true" style="font-size:36px"></i>
        </button>
    </form>
    <span class="m-3" id="id_likes${post.pk}">
        <p style="color:black;">${post.fields.likes.length}</p>
        </span>
        <!-- Dislike -->
        <form action="/comments/post_like_dislike/${post.pk}/" method="GET" class="form-inline dislikeForm" data-pk="${post.pk}">
        <button type="submit" name="submit" value="dislike" title="Dislike" class="btn">
            <i class="fa fa-thumbs-o-down" aria-hidden="true" style="font-size:36px"></i>
        </button>
    </form>
    <span class="m-3" id="id_dislikes${post.pk}">
        <p style="color:black;">${post.fields.dislikes.length}</p>
        </span>
                                `
                                    $('#postsContainer').append(output)
                                }
                            })
                        }
                    }
                })
                // Follwed posts
            } else if ($(window).scrollTop() + $(window).height() == $(document).height() && $('.homepageView.active').html() == 'Followed') {
                $.ajax({
                    url: '',
                    data: {
                        'followed_page': followed_post_page,
                    },
                    method: 'get',
                    dataType: 'json',
                    async: false,
                    success: function (response) {
                        followed_post_page++
                        posts = JSON.parse(response.followed_posts)
                        for (post of posts) {
                            let output = ''
                            $.ajax({
                                url: $('#categoryContainer').attr('data-url'),
                                data: {
                                    'pk': post.fields.user,
                                },
                                method: 'get',
                                dataType: 'json',
                                async: false,
                                success: function (response) {
                                    let user = response.user
                                    let output = ''
                                    let userAvatar = ''
                                    let isOld = ''
                                    if (user.id <= 1000) {
                                        isOld = 'oldUser'
                                    }
                                    if (user.who_see_avatar == 'everyone') {
                                        userAvatar = user.avatar
                                    } else if (user.who_see_avatar == 'friends' && $('#categoryContainer').attr('data-currUser') in JSON.parse(user.friends)) {
                                        userAvatar = user.avatar
                                    } else if ($('#categoryContainer').attr('data-currUser') == user) {
                                        userAvatar = user.avatar
                                    } else {
                                        userAvatar = `/media/profile_images/DefaultUserImage.jpg`
                                    }
                                    output = `
                                    <a href="/people/${user.id}">
        <img src="${userAvatar}" alt="${user.username }" width="64" height="64"
            class="mr-3 float-left rounded-circle ${isOld}" loading="lazy">
            <span>${user.username}</span>
    </a>
    <div class="mb-3">
        <div class="card-body">
                                    `
                                    if (post.fields.description) {
                                        output += `
                                        <blockquote class="blockquote mb-0">
                <p class="text-break">${post.fields.description}</p>
            </blockquote>
                                    `
                                    }
                                    output += `<small class="form-text text-muted">${post.fields.views.length} Views ♦︎ ${ post.fields.post_date }</small>`
                                    if (post.fields.image) {
                                        output += `<img src="/media/${ post.fields.image }" alt="${ user.username }" height="250" width="40%">                                    `
                                    }
                                    if (post.fields.post_file) {
                                        output += `
                                        <video width="100%" controls class="col-md-10 col-lg-8" preload="none">
                <source src="${ post.fields.post_file }" type="video/mp4">
                <source src="/media/${ post.fields.post_file }" type="video/ogg">
                Your browser does not support the video tag.
            </video>
                                    `
                                    }
                                    output += `
                                    </div>
                                </div>
                                <span class="row justify-content-center">
    <span><a href="/comments/${post.pk}" style="text-decoration: none; color:black;"><i
                class="far fa-comment-dots" style="font-size:36px;"></i></a></span>
    <!-- Like -->
    <form method="GET" class="likeForm" class="form-inline" data-pk="${post.pk}">
        <button type="submit" name="submit" value="like" title="Like" class="btn btn-link">
            <i class="fa fa-thumbs-o-up" aria-hidden="true" style="font-size:36px" id="likeButton${post.pk}"></i>
        </button>
    </form>
    <span class="m-3" id="id_likes${post.pk}">
        <p style="color:black;">${post.fields.likes.length}</p>
        </span>
        <!-- Dislike -->
        <form action="/comments/${post.pk}" method="post" class="form-inline"
        id="dislikeForm${post.pk}">
        <button type="submit" name="submit" value="dislike" title="Dislike" class="btn">
            <i class="fa fa-thumbs-o-down" aria-hidden="true" style="font-size:36px"></i>
        </button>
    </form>
    <span class="m-3" id="id_dislikes${post.pk}">
        <p style="color:#065FD4;"><b>${post.fields.dislikes.length}</b></p>
        </span>
                                `

                                }
                            })
                        }
                    }
                })
            }
        }
        bottomScroll();
        $(window).scroll((e) => {
            bottomScroll()
        })
        
    })
})