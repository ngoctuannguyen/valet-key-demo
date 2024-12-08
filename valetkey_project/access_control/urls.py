from django.urls import path
from access_control import views
from access_control.views import generate_valet_key, upload_resource, upload_success
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('valet/<str:key>/', views.access_resource, name='access_resource'),
    # path('upload/', upload_image, name='upload_image'),
    path('generate-valet-key/', views.generate_valet_key, name='generate_valet_key'),
    path('upload/<uuid:valet_key>/', views.upload_resource, name='upload_resource'),
    path('upload/upload-success/', views.upload_success, name='upload_success'),
    path('upload-success/', views.upload_success, name='upload_success'),
    # path('upload/', views.upload_resource, name='upload'),
    path('login/', views.login_view, name='login'),
    path('login-success/', views.valet_key_view, name='valet_key_view'),
    path('resources/', views.resource_list, name='resource_list'),
    path('media/uploads/<path:file_path>', views.protected_media, name='protected_media'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

