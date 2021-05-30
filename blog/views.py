from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Share post via email

    # retrieve post by id and ensure the post has a published status
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    # if request was post we send the email
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)

        # before send check the form is valid or not
        if form.is_valid():
            # Form fields passed validation

            # Get the all data from form
            cd = form.cleaned_data

            # Since you have to include a link to the post in the email,
            # you retrieve the absolute path of the post.
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )

            # Create subject and message
            subject = f"{cd['name']} recommends you read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"

            # Send email
            send_mail(subject, message, 'hopdrmot3@gmail.com', [cd['to']])

            # Sent to true for use that variable later in the template to display a success message
            sent = True

    # if form was GET we send an empty form
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent':sent})

# from django.core import paginator
# from .models import Post
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def post_list(request):
#     # Get all post from published manager
#     # that return those posts status choises is publish.
#     posts = Post.published.all()

#     ########## Page paginator ##########
#     paginator = Paginator(posts, 3)  # n post in each page
#     page = request.GET.get('page') # Get page from url

#     try:
#         posts = paginator.page(page) # Go to that page
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(paginator.num_pages)
#     ########## End page paginator ##########

#     # And return a httpResponse to the page with these modle, and html template
#     return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    # Get these argument for the special post.

    # The get_object_or_404 method get for us a object from model
    # with that argument if does not exist get 404 error
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day,)
    return render(request, 'blog/post/detail.html', {'post': post})
