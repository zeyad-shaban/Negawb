document.addEventListener('DOMContentLoaded', function(){
    window.addEventListener('load', function(){
        $('#editPost').click(function(e){
            e.preventDefault()
            alert('edit')
        })
        $('#deletePost').click(function (e){
            e.preventDefault();
            confirmation = confirm('Permanently delete post?')
            if (confirmation){
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
})
})
