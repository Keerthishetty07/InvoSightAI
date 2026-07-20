from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import InvoiceUploadForm
from .models import Invoice


@login_required(login_url="login")
def upload_invoice(request):

    if request.method == "POST":

        form = InvoiceUploadForm(request.POST, request.FILES)

        if form.is_valid():

            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()

            return redirect("dashboard")

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