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
    "<int:invoice_id>/tally/excel/", views.export_tally_excel_view, name="export_tally_excel",
),
path(
    "<int:invoice_id>/tally/xml/", views.export_tally_xml_view, name="export_tally_xml",
),
path(
    "<int:invoice_id>/tally/json/", views.export_tally_json_view, name="export_tally_json",
),
path(
    "<int:invoice_id>/delete/",
    views.delete_invoice,
    name="delete_invoice",
),
]