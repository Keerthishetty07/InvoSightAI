from django import forms
from .models import Invoice


class InvoiceUploadForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["uploaded_file"]

        widgets = {
            "uploaded_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.jpg,.jpeg,.png"
                }
            )
        }