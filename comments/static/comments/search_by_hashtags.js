document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        let page = 2
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
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:black; display: inline;">${dislikes}</p>`)
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4; display: inline;">${likes}</p>`)
                    } else if (response.action == 'unlike') {
                        likes -= 1
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:black; display: inline;">${likes}</p>`)
                    } else { //Like only
                        likes++
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4; display: inline;">${likes}</p>`)
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
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4; display: inline;">${dislikes}</p>`)
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:black; display: inline;">${likes}</p>`)
                    } else if (response.action === 'undislike') {
                        dislikes -= 1
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:black; display: inline;">${dislikes}</p>`)
                    } else {
                        dislikes++
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4; display: inline;">${dislikes}</p>`)
                    }
                }
            })
        })

        function bottomScroll() {
            if ($(window).scrollTop() + $(window).height() == $(document).height()) {
                let queryString = window.location.search;
                let urlPar = new URLSearchParams(queryString)

                $.ajax({
                    url: window.location.pathname,
                    data: {
                        'page': page,
                        'q': urlPar.get('q')
                    },
                    dataType: 'json',
                    method: 'get',
                    success: function (response) {
                        posts = JSON.parse(response.posts);
                        page++
                        if (posts.length > 0) {
                            for (let i = 0; i < posts.length; i++) {
                                let output = ''
                                $.ajax({
                                    url: $('#mainPosts').attr('data-url'), // {% url 'get_user_by_id' %}
                                    data: {
                                        'pk': posts[i].fields.user,
                                    },
                                    method: 'get',
                                    dataType: 'json',
                                    async: false,
                                    success: function (response) {


                                        let user = response.user
                                        let output = ''
                                        let postCategory = 'All'
                                        if (posts[i].fields.category) {
                                            postCategory = posts[i].fields.category
                                        }
                                        let dateToString = d =>
                                            `${d.getFullYear()}-${('00' + (d.getMonth() + 1)).slice(-2)}-${('00' + d.getDate()).slice(-2)}`
                                        let postDate = new Date(Date.parse(posts[i].fields.post_date))
                                        let date = dateToString(postDate)
                                        output = `

                <div class="card gedf-card">
<div class="card-header">
    <div class="d-flex justify-content-between align-items-center">
        <div class="d-flex justify-content-between align-items-center">
            <div class="mr-2">
                <a href="/people/${user.id}" target='_blank'>
                    <img src="${user.avatar}" alt = ""width="45" class="rounded-circle"
                        loading="lazy">
                </a>
            </div>
            <div class="ml-2">
                <div class="h5 m-0">${user.username}</div>
                <div class="h7 text-muted">${posts[i].fields.views.length} Views -
                    ${postCategory} Topic
                </div>
            </div>
        </div>
        <div>
            <div class="dropdown">
                <button class="btn btn-link" type="button" id="gedf-drop1" data-toggle="dropdown"
                    aria-haspopup="true" aria-expanded="false">
                    <i class="fa fa-ellipsis-h"></i>
                </button>
                <div class="dropdown-menu dropdown-menu-right" aria-labelledby="gedf-drop1">
                    <!-- <div class="h6 dropdown-header">Configuration</div>
                    <a class="dropdown-item" href="#">Save</a>
                    <a class="dropdown-item" href="#">Hide</a>
                    <a class="dropdown-item" href="#">Report</a> -->
                    Under dev
                </div>
            </div>
        </div>
    </div>

</div>
<div class="card-body">
    <div class="text-muted h7 mb-2"> <i class="fa fa-clock-o"></i>${date}</div>
    <!-- Title -->
    <p class="card-link btn-link" href="#">
        <h5 class="card-title">${posts[i].fields.description.substring(0, 45)}</h5>
    </p>
                `
                                        // Image
                                        if (posts[i].fields.image) {
                                            output += `<img src="/media/${posts[i].fields.image}" alt="" style="width:80%; height: auto; margin-left: auto; margin-right: auto;">`
                                        }
                                        // Video
                                        if (posts[i].fields.post_file) {
                                            output += `
                    <video controls class="col-md-10 col-lg-8" preload="none">
        <source src="/media/${posts[i].fields.post_file}" type="video/mp4">
        <source src="/media/${posts[i].fields.post_file}" type="video/ogg">
        Your browser does not support the video tag.
    </video>
                `
                                        }
                                        // Description
                                        if (posts[i].fields.description.length > 45) {
                                            let readMore = '';
                                            if (posts[i].fields.description.length > 227) {
                                                readMore = `<a href="#" class="readMore" data-index=${i}>Read more</a>`;
                                            };
                                            output += `
                    <p class="card-text" style="white-space: pre-line;">
        ${posts[i].fields.description.substring(0, 227)} ${readMore}
    </p>
                `
                                        };

                                        output += `
                </div>
<div class="card-footer">
    <form method="GET" class="likeForm d-inline"
        action="/comments/post_like_dislike/${posts[i].pk}/" data-pk="${posts[i].pk}">
        <button type="submit" class="btn"><i class="far fa-thumbs-up"></i>
            <span id="id_likes${posts[i].pk}">
                <p style="color:black;display: inline">${posts[i].fields.likes.length}</p>
            </span>
            Like</button>
    </form>
    <form action="/comments/post_like_dislike/${posts[i].pk}/" method="GET"
        class="d-inline dislikeForm" data-pk="${posts[i].pk}">
        <button type="submit" class="btn"><i class="far fa-thumbs-down"></i>
            <span id="id_dislikes${posts[i].pk}">
                <p style="color:black; display: inline;">${posts[i].fields.dislikes.length}</p>
            </span>
            Dislike
        </button>
    </form>
    <a href="/comments/${posts[i].pk}/" class="card-link"><i
            class="fab fa-rocketchat"></i>
        Comments</a>
    <!-- AddToAny BEGIN -->
    <a href="https://www.addtoany.com/share#url=https%3A%2F%2Fwww.dfreemedia.com/commetns/${posts[i].pk}&amp;title=${posts[i].fields.description.substring(0, 45)}"
        target="_blank" class="card-link"><i class="fa fa-mail-forward"></i> Share</a>
    <!-- AddToAny END -->
</div>
</div>
            `
                                        $('#mainPosts').append(output)
                                    }
                                })
                            }
                        }

                        function showMore() {
                            $('.readMore').click(function (e) {
                                e.preventDefault();
                                var index = 0;
                                index = $(this).attr('data-index')
                                let thisPost = posts[parseInt(index)]
                                let description = thisPost.fields.description
                                console.log(description)
                                $(this).parent().html(`<br> ${description}`)
                            })
                        }
                        let g = document.createElement('script');
                        let s = document.getElementsByTagName('script')[0]
                        g.text = showMore();
                        s.parentNode.insertBefore(g, s)
                    }
                })
            }
        }
        bottomScroll()
        $(window).scroll(function (e) {
            bottomScroll()
        })
    });
});