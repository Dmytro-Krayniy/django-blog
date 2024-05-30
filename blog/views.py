from django.shortcuts import render
from django.http import HttpRequest

posts = [{'id': 1, 'title': 'Tesla Model 3', 'content': 'Range - 600, price - 40K$', 'updated': '2024/05/24',
          'img_url': 'photos/tesla3.jpeg', 'slug': 'tesla-3'},
         {'id': 2, 'title': 'Hyundai Ionic', 'content': 'Range - 280, price - 14K$', 'updated': '2024/05/23',
          'img_url': 'photos/ionic.jpeg', 'slug': 'hyundai-ionic'},
         {'id': 3, 'title': 'Renault Zoe', 'content': 'Range - 280, price - 10K$', 'updated': '2024/05/25',
          'img_url': 'photos/zoe.jpeg', 'slug': 'renault-zoe'},
        ]


def index(request: HttpRequest):
    return render(request, 'blog/index.html', context={'posts': posts})


def show_post(request: HttpRequest, slug):
    post = posts[0]
    for p in posts:
        if p['slug'] == slug:
            post = p
    return render(request, 'blog/post_detail.html', context={'post': post})


def contact(request: HttpRequest):
    return render(request, 'blog/contact.html')


def thanks(request: HttpRequest):
    return render(request, 'blog/thanks.html')


def signup(request: HttpRequest):
    return render(request, 'blog/signup.html')


def signin(request: HttpRequest):
    return render(request, 'blog/signin.html')


def search(request: HttpRequest):
    return render(request, 'blog/search.html')
