from django.urls import path
from . import views

urlpatterns = [
    path(
        "upload/",
        views.upload_bank,
        name="upload_bank"
    ),
]