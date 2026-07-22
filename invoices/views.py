from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import InvoiceUploadForm
from .models import Invoice
from .services import process_invoice

from .edit_forms import InvoiceEditForm
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

    invoices = Invoice.objects.filter(
        user=request.user
    ).order_by("-created_at")

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
            "invoice": invoice
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