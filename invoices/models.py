from django.db import models
from django.contrib.auth.models import User


class Invoice(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processed", "Processed"),
        ("Failed", "Failed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    invoice_number = models.CharField(
        max_length=100,
        blank=True
    )

    vendor = models.CharField(
        max_length=255,
        blank=True
    )

    gst_number = models.CharField(
        max_length=100,
        blank=True
    )

    invoice_date = models.DateField(
        null=True,
        blank=True
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    currency = models.CharField(
        max_length=20,
        default="INR"
    )

    uploaded_file = models.FileField(
        upload_to="uploads/invoices/"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.vendor} - {self.invoice_number}"
