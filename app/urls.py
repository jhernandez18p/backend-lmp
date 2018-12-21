from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve


urlpatterns = [
    path('', include('src.base.urls')),
    path('accounts/', include('src.users.urls',namespace='auth')),
    path('intra/', include('src.intra.urls')),
    path('api/v2/', include('src.api.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

admin.site.site_title = 'Dev2tech CMS'
admin.site.site_header = 'Luxury Motors Panamá'

handler404 = 'src.base.views.page_not_found_view'
handler500 = 'src.base.views.error_view'
handler403 = 'src.base.views.permission_denied_view'
handler400 = 'src.base.views.bad_request_view'