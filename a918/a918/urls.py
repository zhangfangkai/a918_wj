from django.conf.urls import include, url
from django.contrib import admin
from views import *
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'ztf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', total_view),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^DA/', include('DA.urls')),
    url(r'^wenjuan/',include('wenjuan.urls')),
    url(r'^count/',include('count.urls')),

]
