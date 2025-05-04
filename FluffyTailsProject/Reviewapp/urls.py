from django.urls import path
from . import views
urlpatterns = [
    path('contactus/', views.contact_view, name='contactus'),
]

