from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from blog.views import common



urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls')),
<<<<<<< HEAD
    url(r'^$', common.index, name='main_index'),
=======
    url(r'^$', views.index, name='main_index'),
>>>>>>> 98adf8242f75a50d948056c25c0a6dc59ffc2b33


)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_PATH)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT})

    )
