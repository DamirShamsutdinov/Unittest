from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User

LENGTH = 10


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, LENGTH)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "title": "Последние обновления на сайте"
        # на начало спринта_5 было "posts": posts
    }
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, LENGTH)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "group": group,
        "title": "Все записи группы",
        # на начало спринта_5 было "posts": posts
        "page_obj": page_obj,
    }
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()
    paginator = Paginator(post_list, LENGTH)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "user": user,
        "post_list": post_list,
        "page_obj": page_obj,
        "author": user,
    }
    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_count = post.author.posts.count()
    context = {
        "post": post,
        "post_count": post_count,
    }
    return render(request, "posts/post_detail.html", context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("posts:profile", username=request.user)
    context = {"form": form}
    return render(request, "posts/create_post.html", context)


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if post.author != request.user:
        return redirect("posts:post_detail", post_id)
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post_id)
    context = {
        "form": form,
        "is_edit": is_edit,
    }
    return render(request, "posts/create_post.html", context)
