from django import forms
from .models import Invoice


class InvoiceEditForm(forms.ModelForm):
    class Meta:
        model = Invoice

        fields = [
            "invoice_number",
            "vendor",
            "customer",
            "vendor_gstin",
            "customer_gstin",
            "invoice_date",
            "due_date",
            "subtotal",
            "tax",
            "total",
            "status",
        ]

        widgets = {
            "invoice_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }