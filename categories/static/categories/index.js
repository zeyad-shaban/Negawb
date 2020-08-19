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

    let homepage_post_page = 2

    function bottomScroll() {
        if ($(window).scrollTop() + $(window).height() == $(document).height()) {
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
                            data:{
                                'pk': post.fields.user,
                            },
                            method: 'get',
                            dataType: 'json',
                            async: false,
                            success: function (response){
                                let user = response.user
                                let output = ''
                                let userAvatar = ''
                                if (user.who_see_avatar == 'everyone'){
                                    userAvatar = `<img src="${ user.avatar }" alt="${ user.username }" widht="64" height="64" class="mr-3 float-left">`
                                }
                                else if (user.who_see_avatar == 'friends' && $('#categoryContainer').attr('data-currUser') in JSON.parse(user.friends)){
                                    userAvatar = user.avatar
                                }
                                else if ($('#categoryContainer').attr('data-currUser') == user){
                                    userAvatar = user.avatar
                                }
                                else {
                                    userAvatar = `/media/profile_images/DefaultUserImage.WebP`
                                }
                                if (post.fields.image){
                                    output = `
                                        <a href="/people/${user.id}">
                                        <img src="${userAvatar}" alt="${ user.username }" widht="64" height="64" class="mr-3 float-left">
                                            <span>${user.username}</span>
                                        </a>
                                        <div class="mb-3">
                                            <div class="card-body">
                                                <p class="card-text">${post.fields.description}</p>
                                                <img src="/media/${ post.fields.image }" alt="${ user.username }" height="250" width="40%">
                                                <p class="card-text"><small class="form-text text-muted">Published at ${ post.fields.post_date}</small>
                                                </p>
                                            </div>
                                        </div>
                                    `
                                } else if (post.fields.post_file){
                                    output = `
<a href="/people/${user.id}/">
    <img src="${ userAvatar }" alt="${ user.username }" widht="64" height="64" class="mr-3 float-left">
    <span>${user.username}</span>
</a>
<div class="mb-3">
    <div class="card-body">
        <p class="card-text">${ post.fields.description }</p>
        <video width="400" height="320" controls>
            <source src="/media/${ post.fields.post_file }" type="video/mp4">
            <source src="/media/${ post.fields.post_file }" type="video/ogg">
            Your browser does not support the video tag.
        </video>
        <p class="card-text"><small class="form-text text-muted">Published at ${ post.fields.post_date}</small>
        </p>
    </div>
</div>
                                    `
                                } else if (post.fields.description && !post.fields.post_file && !post.fields.image){
                                    output = `
<div class="card">
    <div class="card-header">
        <a href="/people/${user.id}/">
            <img src="${ user.avatar }" alt="${ user.username }" widht="64" height="64"
                class="mr-3 float-left">
            ${ user.username }
        </a>
    </div>
    <div class="card-body">
        <blockquote class="blockquote mb-0">
            <p class="text-break">${ post.fields.description }</p>
            <small class="form-text text-muted">Published at ${ post.fields.post_date }</small>
        </blockquote>
    </div>
</div>
                                    `
                                }
                                output += `
                                <span class="row justify-content-center">
    <span><a href="/comments/${post.pk}" style="text-decoration: none; color:black;"><i
                class="far fa-comment-dots" style="font-size:36px;"></i></a></span>
    <!-- Like -->
    <form method="GET" id="likeForm${post.pk}" class="form-inline" data-pk="${post.pk}">
        <button type="submit" name="submit" value="like" title="Like" class="btn btn-link">
            <i class="fa fa-thumbs-o-up" aria-hidden="true" style="font-size:36px" id="likeButton${post.pk}"></i>
        </button>
    </form>
    <span class="m-3" id="id_likes${post.pk}">
        <p style="color:#065FD4;"><b>${post.fields.likes.length}</b></p>
        <p style="color:black;">${post.fields.likes.length}</p>
        </span>
        <!-- Dislike -->
    <form action="{% url 'comments:post_like_dislike" method="post" class="form-inline"
        id="dislikeForm{{post.id}}">
        {% csrf_token %}
        <button type="submit" id="dislikeButton{{post.id}}" name="submit" value="dislike" title="Dislike" class="btn">
            <i class="fa fa-thumbs-o-down" aria-hidden="true" style="font-size:36px"></i>
        </button>
    </form>
    <span class="m-3" id="id_dislikes{{post.id}}">
        {% if user in post.dislikes.all %}
        <p style="color:#065FD4;"><b>{{post.dislikes.count}}</b></p>
        {% else %}
        <p style="color:black;">{{post.dislikes.count}}</p>
        {% endif %}
    </span>
                                `
                                $('#postsContainer').append(output)
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