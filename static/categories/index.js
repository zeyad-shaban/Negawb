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
                    i++
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
                                    userAvatar = `<img src="${ user.avatar }" alt="${ user.username }" widht="64" height="64" class="mr-3 float-left">`
                                }
                                else if ($('#categoryContainer').attr('data-currUser') == user){
                                    userAvatar = `<img src="${ user.avatar }" alt="${ user.username }" widht="64" height="64" class="mr-3 float-left">`
                                }
                                else {
                                    userAvatar = `<img src="/media/profile_images/DefaultUserImage.WebP" alt="${ user.username }" widht="64" height="64" class="mr-3 float-left">`
                                }
                                if (post.fields.image){
                                    output = `
                                    <a href="/people/${user.id}">
                                    ${userAvatar}
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
                                }
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