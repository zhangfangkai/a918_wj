from django.conf.urls import include, url
from views import *

urlpatterns = [
    url(r'^$', main),
    url(r'zhuanye/', zy),
    url(r'xueshu/', xs),
    url(r'daxue/', zdx),
    url(r'ml/', ml),
    url(r'xk/', xk),
    url(r'result/', result),
    url(r'tx/', tx),
    url(r'cx/', cx),

]
