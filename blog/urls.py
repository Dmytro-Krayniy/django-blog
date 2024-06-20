from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path

from blog import views
from myblog import settings

urlpatterns = [
    path('', views.MainPage.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/success/', views.thanks, name='success'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('tag/<slug:tag_slug>/', views.TagList.as_view(), name='tag_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
