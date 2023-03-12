from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from datetime import datetime

from . import models
from .forms import AddrequestForm, RegisterForm
from django.contrib.auth.models import Group


@login_required
def new_request(request):
    data = models.Form.objects.filter(user=request.user).order_by("-time")[:5]
    if request.method == "POST":
        form = AddrequestForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form = AddrequestForm()
    else:
        form = AddrequestForm()
    return render(request, "req.html", {"form": form, "data": data})


@staff_member_required
def get_all_requests(request):
    data = (
        models.Form.objects.filter(active=True)
        .order_by("-priority","time")
        .select_related("implementer", "user")
        .prefetch_related("soimplementor")
    )
    return render(request, "watchdog.html", {"data": data})


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("new")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name = form.cleaned_data['groups'])
            user.groups.add(group)
            login(request, user)
            return redirect("new")
    else:
        form = RegisterForm()
    return render(request, "registration/sign_up.html", {"form": form})





@require_POST
@staff_member_required
def takereq(request, id):
    req = models.Form.objects.get(pk=id)
    req.state = "В работе"
    if req.implementer is None:
        req.implementer = request.user
    req.save()
    return redirect("requests")


@require_POST
@staff_member_required
def complitedreq(request, id):
    req = models.Form.objects.get(pk=id)
    req.active = False
    req.state = "Завершено"
    req.done_at = datetime.now().date()
    req.save()
    return redirect("requests")


@require_POST
@staff_member_required
def sub_implementor(request, id):
    req = models.Form.objects.get(pk=id)
    if req.active == True:
        req.soimplementor.add(request.user)
    return redirect("requests")
