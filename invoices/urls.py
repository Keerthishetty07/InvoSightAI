from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_invoice, name="upload_invoice"),
    path("history/", views.invoice_list, name="invoice_history"),
    path("<int:invoice_id>/",views.invoice_detail,name="invoice_detail"),
    path("<int:invoice_id>/file/", views.serve_invoice_file, name="invoice_file"),
    path(
    "<int:invoice_id>/edit/",
    views.edit_invoice,
    name="edit_invoice"
),
path(
    "export/csv/",
    views.export_csv,
    name="export_csv",
),
path(
    "<int:invoice_id>/delete/",
    views.delete_invoice,
    name="delete_invoice",
),
]