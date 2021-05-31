from django import template
from django.db.models.expressions import Ref
from ..models import Post
from django.db.models import Count

register = template.Library()

# Custom template tags


@register.simple_tag
# Django will use the function's name as the tag name. If you want to register it using a different name,
# you can do so by specifying a name attribute,
# such as @register.simple_tag(name='my_tag').
def total_posts():
    # retrieve count of published post
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
# specify the template that will be rendered with the returned values
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts, }


@register.simple_tag
def get_most_comments_posts(count=5):
    # annotate() function to aggregate the total number of comments for each post.

    return Post.published.annotate(
        # You use the Countaggregation function to store the number of comments
        # in the computed field total_comments for each Post object
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]
