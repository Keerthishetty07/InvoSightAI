from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def upload_bank(request):
    return render(
        request,
        "bank/upload_bank.html"
    )
