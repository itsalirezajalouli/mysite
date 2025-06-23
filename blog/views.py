from .models import Post
from django.core.mail import send_mail
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger

lass PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request: HttpRequest) -> HttpResponse:
    post_list = Post.published.all()
    items_per_page = 3
    paginator = Paginator(post_list, items_per_page)
    page_number = request.GET.get('page', 1)                                        # get pn, 1 post as default

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)                                 
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)                                 # when out of range go to last

    return render(request, 'blog/post/list.html', { 'posts': posts})                # req obj, temp path, cntxt var

def post_detail(request: HttpRequest, year: int, month: int, day: int,
                post: str) -> HttpResponse:
    post = get_object_or_404(Post,
                             status = Post.Status.PUBLISHED,
                             slug = post,
                             publish__year = year,
                             publish__month = month,
                             publish__day = day)

    # the reason we can use post.comment is we defined comments as manager when
    # we set related_name of foreign key to comments in Comment model
    comments = post.comments.filter(active = True)                                  # this is a queryset
    form = CommentForm()
    return render(request, 'blog/post/detail.html',
                  { 'post': post, 'comments': comments, 'form': form }) 

def post_share(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post,                                                  # first time page loads, this
                             id = post_id,                                          # view receives a GET request
                             status = Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)                                          # form was submitted
        if form.is_valid():                                                         # form.errors -> validation errs
            cd = form.cleaned_data                                                  # a dic of normalized fields

            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())          # makes complete url including
                                                                                    # http schema and hostname
            subject = (f'{cd['name']} ({cd['email']}) '
                       f'recommended you read {post.title}')
            message = (f'Read {post.title} {post_url}\n\n'
                       f'{cd['name']}\'s comment: {cd['comment']}')
            send_mail(subject = subject,
                      message = message,
                      from_email = None,                                            # default in .env will be used
                      recipient_list = [cd['to']])
            sent = True

    else:
        form = EmailPostForm()                                                      # first time -> empty form

    return render(request, 'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})

@require_POST                                                                       # only allow POST | else 405
def post_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post,
                             id = post_id,
                             status = Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data = request.POST)
    if form.is_valid():
        comment = form.save(commit = False)                                         # create but not save to db
        comment.post = post                                                         # assign post to comment
        comment.save()                                                              # save to db
    return render(request, 'blog/post/comment.html',
                  {'post': post, 'form': form, 'comment': comment})

