from django.shortcuts import render


def prices(request):
    return render(request, "pages/prices.html", {})


def storage_rules(request):
    return render(request, "pages/storage_rules.html", {})


def addresses(request):
    return render(request, "pages/addresses.html", {})


def testimonials(request):
    return render(request, "pages/testimonials.html", {})


def legal(request):
    return render(request, "pages/legal.html", {})


def contacts(request):
    return render(request, "pages/contacts.html", {})
