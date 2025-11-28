from django.http import HttpRequest
from django.shortcuts import redirect, render

from lists.models import Item


def home_page(request: HttpRequest):
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/")

    return render(
        request,
        "home.html",
        {"new_item_text": request.POST.get("item_text", "")},
    )
