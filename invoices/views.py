from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import InvoiceUploadForm
from .models import Invoice
from .services import process_invoice
from django.contrib import messages
import csv
from django.http import HttpResponse, FileResponse, Http404
from pathlib import Path
import mimetypes
from django.conf import settings

from .edit_forms import InvoiceEditForm
from .tally_exports import export_tally_excel, export_tally_xml, export_tally_json
@login_required(login_url="login")
def upload_invoice(request):

    if request.method == "POST":

        form = InvoiceUploadForm(request.POST, request.FILES)

        if form.is_valid():

            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            process_invoice(invoice)
            return redirect("invoice_history")

    else:
        form = InvoiceUploadForm()

    return render(
        request,
        "invoice/upload.html",
        {
            "form": form
        }
    )
@login_required(login_url="login")
def invoice_list(request):

    q = request.GET.get("q")

    invoices = Invoice.objects.filter(
        user=request.user
    )

    if q:

        invoices = invoices.filter(
            vendor__icontains=q
        ) | invoices.filter(
            invoice_number__icontains=q
        )

    invoices = invoices.order_by("-created_at")

    return render(
        request,
        "invoice/invoice_list.html",
        {
            "invoices": invoices
        }
    )
from django.shortcuts import get_object_or_404

@login_required(login_url="login")
def invoice_detail(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        user=request.user
    )

    return render(
        request,
        "invoice/invoice_details.html",
        {
            "invoice": invoice,
            "invoice_media_url": f"/invoices/{invoice.id}/file/",
        }
    )
@login_required(login_url="login")
def edit_invoice(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        user=request.user
    )

    if request.method == "POST":

        form = InvoiceEditForm(
            request.POST,
            instance=invoice
        )

        if form.is_valid():

            print("Form is valid")

            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()

            print("Invoice saved")

            process_invoice(invoice)
            

            messages.success(
                request,
                "Invoice uploaded and processed successfully."
            )

            

            print("Processing finished")

            return redirect("invoice_history")

        else:

            print("FORM ERRORS:")
            print(form.errors)

    return render(
        request,
        "invoice/edit_invoice.html",
        {
            "form": form,
            "invoice": invoice
        }
    )

@login_required
def export_csv(request):

    invoices = Invoice.objects.filter(user=request.user)

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = 'attachment; filename="invoices.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Invoice",
        "Vendor",
        "Customer",
        "Date",
        "Total",
        "Status"
    ])

    for invoice in invoices:

        writer.writerow([
            invoice.invoice_number,
            invoice.vendor,
            invoice.customer,
            invoice.invoice_date,
            invoice.total,
            invoice.status
        ])

    return response


@login_required(login_url="login")
def serve_invoice_file(request, invoice_id):
    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        user=request.user,
    )

    file_path = Path(invoice.uploaded_file.path)
    media_root = Path(settings.MEDIA_ROOT).resolve()

    try:
        file_path.resolve().relative_to(media_root)
    except ValueError:
        raise Http404("Invalid file path")

    if not file_path.exists() or not file_path.is_file():
        raise Http404("Invoice file not found")

    content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    response = FileResponse(
        open(file_path, "rb"),
        as_attachment=False,
        filename=file_path.name,
        content_type=content_type,
    )
    return response

@login_required
def delete_invoice(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        user=request.user
    )

    invoice.delete()

    return redirect("invoice_history")

@login_required(login_url="login")
def export_tally_excel_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    return export_tally_excel(invoice)


@login_required(login_url="login")
def export_tally_xml_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    return export_tally_xml(invoice)


@login_required(login_url="login")
def export_tally_json_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    return export_tally_json(invoice)
