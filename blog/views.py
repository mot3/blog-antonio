from django.core import paginator
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    # Get all post from published manager
    # that return those posts status choises is publish.
    posts = Post.published.all()

    ########## Page paginator ##########
    paginator = Paginator(posts, 3)  # n post in each page
    page = request.GET.get('page') # Get page from url

    try:
        posts = paginator.page(page) # Go to that page
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(paginator.num_pages)
    ########## End page paginator ##########

    # And return a httpResponse to the page with these modle, and html template
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    # Get these argument for the special post.

    # The get_object_or_404 method get for us a object from model
    # with that argument if does not exist get 404 error
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day,)
    return render(request, 'blog/post/detail.html', {'post': post})
