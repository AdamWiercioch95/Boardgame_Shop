from django.urls import path
from accounts import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
]


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', TemplateView.as_view(template_name='landing_page.html'), name='landing_page'),
#     # j.w. zakładka 'kontakt' oraz 'o stronie'
#     path('accounts/', include('accounts.urls')),
#     path('shop/', include('shop.urls')),
# ]