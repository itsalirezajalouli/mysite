import markdown
from .models import Post    
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.template.defaultfilters import truncatewords_html

class LatestPostsFeed(Feed):                                                        # each filed corresponds to
    title = 'My Blog'                                                               # <title> rss element
    link = reverse_lazy('blog:post_list')                                           # <link> rss element
    description = 'New posts of my blog.'                                           # <description> rss element

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_update(self, item):
        return item.publish
