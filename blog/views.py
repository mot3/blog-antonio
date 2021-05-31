from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm, CommentForm
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from taggit.models import Tag
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger
from django.db.models import Count


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

        # Get the from from post
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

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_list(request, tag_slug=None):
    # Get all post from published manager
    # that return those posts status choises is publish.
    posts = Post.published.all()

    tag = None
    if tag_slug:
        # if tag_slug was full

        # Get tags from tag table
        tag = get_object_or_404(Tag, slug=tag_slug)

        # filter posts by tags
        posts = posts.filter(tags__in=[tag])

    ########## Page paginator ##########
    paginator = Paginator(posts, 3)  # n post in each page
    page = request.GET.get('page')  # Get page from url

    try:
        posts = paginator.page(page)  # Go to that page
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(paginator.num_pages)
    ########## End page paginator ##########

    # And return a httpResponse to the page with these modle, and html template
    return render(request, 'blog/post/list.html', {'posts': posts,
                                                   'tag': tag, })


def post_detail(request, year, month, day, post):
    # Get these argument for the special post.

    # The get_object_or_404 method get for us a object from model
    # with that argument if does not exist get 404 error
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,)

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None
    comment_form = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the databese
            new_comment.save()

        else:
            comment_form = CommentForm()

    # List of similar posts

    # You retrieve a Python list of IDs for the tags of the current post.
    # The values_list() QuerySet returns tuples with the values for the given fields.
    # You pass flat=True to it to get single values such as [1, 2, 3, ...]
    # instead of one-tuples such as [(1,), (2,), (3,) ...].
    post_tags_ids = post.tags.values_list('id', flat=True)

    #You get all posts that contain any of these tags, excluding the current post itself.
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)

    # You use the Count aggregation function to generate a calculated field—same_tags—
    # that contains the number of tags shared with all the tags queried.
    # find the more same tag
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts,})
