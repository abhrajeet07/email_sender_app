from django.urls import path
from .views import send_email  # Update this line

urlpatterns = [
    path('', send_email, name='send_email'),  # Ensure this path is correctly named
]
