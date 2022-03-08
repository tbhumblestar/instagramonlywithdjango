
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login_required(TemplateView.as_view(template_name='root.html')),name='root'),
    path('accounts/',include('accounts.urls'))
    #re_path('',TemplateView.as_view(template_name='root.html'),name='root')
    #re_path('')는 모든 주소에 대해서임(정규표현식 > 빈문자열 > 모든문자열)
]

#debug가 켜져있다면, setting의 설정에 따라 media파일들의 위치 및 링크를 사용하겠다는 것임
if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    