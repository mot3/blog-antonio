from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = 'My blog'

    # The reverse_lazy()utility function is a lazily evaluated version of reverse().
    # It allows you to use a URL reversal before the project's URL configuration is loaded.
    link = reverse_lazy('blog:post_list')

    description = 'New posts of my blog'

    def items(self):
        # The items() method retrieves the objects to be included in the feed.
        # You are retrieving only the last five published posts for this feed.
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
