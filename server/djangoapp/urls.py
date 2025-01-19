from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration

    # path for login
    # API endpoint for login logic
    path('api/login/', views.login_user, name='login_api'),
    # React frontend route for login
    path('login/', TemplateView.as_view(template_name="index.html")),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
