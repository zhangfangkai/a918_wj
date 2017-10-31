from django.conf.urls import include, url
from views import *

urlpatterns = [

    url(r'^$', login),
    url(r'^login',login),
    url(r'^mainpage', mainpage),
    url(r'^wjmanage', wjmanage),
#---- zfk add at 2017-08-31
    url(r'^wjadd', wjadd),
    url(r'^surveysave', surveysave),
    url(r'^optisave', optisave),
    url(r'^wjview', wjview),
    url(r'^dataimp', dataimp),
    url(r'^wjdel',wjdel),
    url(r'^wjfabu',wjfabu),
    url(r'^wjmodify',wjmodify),
#----
#---- zyz add at 2017-08-11
	url(r'^bgraph', bgraph),
    url(r'^makeZxt', make_zxt),
    url(r'^options/', show_options),
#---- at 2017-09-03
    url(r'^subvari', submitvari),
    url(r"^subqpt",submitqpt),

#----zfk add at 2017-9-3
    url(r'^ldt_canshu', ldt_data),


#---- hbt add at 2017-9-3
    url(r'basic', basic_mainpage),
    url(r'wenjuan', wenjuan_analyse),
    url(r'^analyse_options/', show_options_analyse),
    url(r'result', analyse_result),

    url(r'submit_map', submit_map),
#----
]
