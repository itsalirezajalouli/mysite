from . import views
from django.urls import path
from .feeds import LatestPostsFeed

app_name = 'blog'                                                                   # for settings to detect this

urlpatterns = [
        path('', views.post_list, name = 'post_list'),                              # str pattern, view, url name
        # path('', views.PostListView.as_view(), name = 'post_list'),
        path('<int:year>/<int:month>/<int:day>/<slug:post>',
             views.post_detail,
             name = 'post_detail'),
        path('<int:post_id>/share', views.post_share, name = 'post_share'),
        path('<int:post_id>/comment', views.post_comment, name = 'post_comment'),
        path('feed/', LatestPostsFeed(), name = 'post_feed'),
        path('tag/<slug:tag_slug>/', views.post_list, name = 'post_list_by_tag'),   # 2 pattern point to same view
        path('search/', views.post_search, name = 'post_search'),
    ]
