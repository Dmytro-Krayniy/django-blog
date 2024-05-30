from django.conf.urls.static import static
from django.urls import path

from blog import views
from myblog import settings

urlpatterns = [
    path('', views.index, name='home'),
    path('post/<slug:slug>/', views.show_post, name='show_post'),
    path('contact/', views.contact, name='contact'),
    path('contact/thanks/', views.thanks, name='thanks'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('search/', views.search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
