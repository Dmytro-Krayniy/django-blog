from django.contrib.auth import login, authenticate
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from taggit.models import Tag

from blog.forms import SignUpForm, SignInForm, ContactForm, CommentForm
from blog.models import Post, Comment


# posts = [{'id': 1, 'title': 'Tesla Model 3', 'content': 'Range - 600, price - 40K$', 'updated': '2024/05/24',
#           'img_url': 'photos/tesla3.jpeg', 'slug': 'tesla-3'},
#          {'id': 2, 'title': 'Hyundai Ionic', 'content': 'Range - 280, price - 14K$', 'updated': '2024/05/23',
#           'img_url': 'photos/ionic.jpeg', 'slug': 'hyundai-ionic'},
#          {'id': 3, 'title': 'Renault Zoe', 'content': 'Range - 280, price - 10K$', 'updated': '2024/05/25',
#           'img_url': 'photos/zoe.jpeg', 'slug': 'renault-zoe'},
#         ]


class MainPage(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_at')
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return render(request, 'blog/index.html', context={'page_obj': page})


# def index(request: HttpRequest):
#     return render(request, 'blog/index.html', context={'posts': posts})


class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('-created_at')[:5]
        comment_form = CommentForm()
        return render(request, 'blog/post_detail.html',
                      context={'post': post,
                               'common_tags': common_tags,
                               'last_posts': last_posts,
                               'comment_form': comment_form
                               }
                      )
    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST.get('text')
            username = self.request.user
            post = get_object_or_404(Post, url=slug)
            Comment.objects.create(text=text, username=username, post=post)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'blog/post_detail.html',
                      context={'comment_form': comment_form}
                      )

class ContactView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, 'blog/contact.html', context={'form': form, 'title': 'Contact us'})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'From {name} | {subject}', message, email, ['dmkrayniy@ukr.net'])
            except BadHeaderError:
                return HttpResponse('invalid e-mail data')
            return HttpResponseRedirect('success')
        return render(request, 'blog/contact.html', context={'form': form, 'title': 'Contact us'})


def thanks(request: HttpRequest):
    return render(request, 'blog/thanks.html')

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'blog/signup.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
        return render(request, 'blog/signup.html', context={'form': form})


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'blog/signin.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
        return render(request, 'blog/signin.html', context={'form': form})


class SearchResultsView(ListView):
    template_name = 'blog/search.html'
    model = Post
    paginate_by = 4
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        results = []
        if query:
            results = Post.objects.filter(Q(h1__icontains=query) | Q(description__icontains=query) |
                                          Q(content__icontains=query))
        return results


class TagList(ListView):
    paginate_by = 5
    template_name = 'blog/tags.html'
    context_object_name = 'posts'
    model = Post

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        posts = Post.objects.filter(tag=tag)
        return posts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '#Tag: ' + self.kwargs['tag_slug']
        context['tag_selected'] = self.kwargs['tag_slug']
        context['common_tags'] = Post.tag.most_common()
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h2>Page not found</h2> exception: {exception}')
