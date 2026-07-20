from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_invoice, name="upload_invoice"),
    path("history/", views.invoice_list, name="invoice_history"),
]