from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import json
from invoices.models import Invoice


def home(request):
    return render(request, "home.html")


@login_required(login_url="login")
def dashboard(request):

    invoices = Invoice.objects.filter(user=request.user)

    total_invoices = invoices.count()

    processed = invoices.filter(status="Processed").count()

    pending = invoices.filter(status="Pending").count()

    failed = invoices.filter(status="Failed").count()

    total_amount = invoices.aggregate(
        Sum("total")
    )["total__sum"] or 0

    recent_invoices = invoices.order_by("-created_at")[:5]
    monthly_expenses = (
        invoices
        .annotate(month=TruncMonth("invoice_date"))
        .values("month")
        .annotate(total=Sum("total"))
        .order_by("month")
    )
    context = {
        "total_invoices": total_invoices,
        "processed": processed,
        "pending": pending,
        "failed": failed,
        "total_amount": total_amount,
        "recent_invoices": recent_invoices,

        "months": json.dumps([
            item["month"].strftime("%b %Y")
            for item in monthly_expenses
            if item["month"]
        ]),

        "monthly_totals": json.dumps([
            float(item["total"])
            for item in monthly_expenses
        ]),
        "status_labels": json.dumps([
            "Processed",
            "Pending",
            "Failed"
        ]),

        "status_values": json.dumps([
            processed,
            pending,
            failed
        ]),
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )