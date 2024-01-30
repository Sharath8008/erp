from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('home', views.home, name="home"),
    path('logoutuser/', views.logoutuser, name="logout"),
    path('upload/', views.upload, name='upload'),
    path('Inventory/', views.Inventory, name='Inventory'),
    path('hr/', views.hr, name='hr'),
    path('crm/', views.crm, name='crm'),
    path('fm/', views.fm, name='fm'),
    path('reports/', views.reports, name='reports'),
    path('scm/', views.scm, name='scm'),
    path('modify/', views.modify, name='modify'),  # Modify the URL pattern
    path('get_axes_options/', views.get_axes_options, name='get_axes_options'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)