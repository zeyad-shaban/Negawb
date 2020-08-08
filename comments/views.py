from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404, HttpResponse
from django.forms.models import model_to_dict
from categories.models import Category
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, PostForm
from django.db.models import Q
from django.contrib import messages


# todo make this view only function (NO CREATING)
def posts(request):
    posts = Post.objects.all().order_by('-post_date')
    if request.method == 'GET':
        return render(request, 'comments/posts.html', {'posts': posts, 'form': PostForm})
    # Add Post

    elif request.POST['submit'] == 'Add Comment':
        try:
            form = PostForm(request.POST)
            post = form.save(commit=False)
            post.user = request.user
            messages.success(request, "created post successfully")
            post.save()
            return redirect('comments:posts')
        except ValueError:
            messages.error(request, 'Title must be 0-40 character')
            return redirect('comments:posts')


@login_required
def view_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(
        post=post).order_by('-comment_date')[:150]
    if request.method == 'GET':
        return render(request, 'comments/view_post.html', {'post': post, 'comments': comments, 'form': CommentForm})
    else:
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        return redirect('comments:view_post', pk=pk)


def results_post(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'comments/results_post.html', {'posts': posts, 'form': PostForm})


@login_required
def post_like_dislike(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # Like
    if request.GET.get('submit') == 'like':
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
            post.likes.add(request.user)
            return JsonResponse({'action': 'undislike_and_like'})
        elif request.user in post.likes.all():
            post.likes.remove(request.user)
            return JsonResponse({'action': 'unlike'})
        else:
            post.likes.add(request.user)
            return JsonResponse({'action': 'like_only'})
    # Dislike
    elif request.GET.get('submit') == 'dislike':
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            post.dislikes.add(request.user)
            return JsonResponse({'action': 'unlike_and_dislike'})
        elif request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
            return JsonResponse({'action': 'undislike'})
        else:
            post.dislikes.add(request.user)
            return JsonResponse({'action': 'dislike_only'})


# todo fix MultiDictValue
@login_required
def reply_like_dislike(request, reply_id):
    reply = get_object_or_404(Comment, pk=reply_id)
    # Dislike
    if request.POST['submit'] == 'dislike':
        if request.user in reply.likes.all():
            reply.likes.remove(request.user)
            reply.dislikes.add(request.user)
            messages.success(request, 'Disliked')
            return redirect('comments:reply_like_dislike', reply_id)
        elif request.user in reply.dislikes.all():
            reply.dislikes.remove(request.user)
            messages.success(request, 'Removed Disliked')
            return redirect('comments:reply_like_dislike', reply_id)
        else:
            reply.dislikes.add(request.user)
            messages.success(request, 'Disliked')
            return redirect('comments:reply_like_dislike', reply_id)
    # Like
    else:
        if request.user in reply.dislikes.all():
            reply.dislikes.remove(request.user)
            reply.likes.add(request.user)
            messages.success(request, 'liked')
        elif request.user in reply.likes.all():
            reply.likes.remove(request.user)
            messages.success(request, 'removed like')
        else:
            reply.likes.add(request.user)
            messages.success(request, 'liked')
        return redirect('comments:reply_like_dislike', reply_id)


def create_post(request, pk):
    category = get_object_or_404(Category, pk=pk)
    #! NOT SERIALIZING IMAGES
    # Images category
    if request.user.max_posts >= 3:
        messages.error(
            request, f'You can only make 3 posts a day, please wait till tommorow')
        return redirect('categories:view_category', pk=pk)
    else:
        # if pk == 1:
        #     image = request.GET.get('image')
        #     description = request.GET.get('description')
        #     if image:
        #         if description:
        #             post = Post(description=description, image=image,
        #                         user=request.user, category=category)
        #             post.save()
        #         else:
        #             post = Post(description=description,
        #                         user=request.user, category=category)
        #             post.save()
        #     else:
        #         # todo return error
        #         pass
        #  Fun Area Category
        if pk == 2:
            post = Post(user=request.user, category=category)
            if request.POST['description']:
                post.description = request.POST['description']
                post.save()
                request.user.max_posts += 1
                messages.warning(request, request.user.max_posts)
            if request.POST['image'] and request.POST['post_file']:
                messages.error(request, 'You can\'t have both image and file')
            elif request.POST['image']:
                post.image = request.POST['image']
                post.save(instance=post)
                
            elif request.POST['post_file']:
                post.post_file = request.POST['post_file']
                post.save(instance=post)
                

            return redirect('categories:view_category', pk=category.id)

        # TRUSTED NEWS
        elif pk == 4:
            if not request.user.is_confirmed:
                return HttpResponse('You are not a confirmed source, IF YOU FOUND A GLITCH THAT ALLOWS YOU TO MAKE POSTS HERE REPORT IT AS SOON AS POSSIBLE AND DO NOT MAKE ANY USE OF IT!')
