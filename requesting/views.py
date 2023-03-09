from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from . import models
from .forms import AddrequestForm, RegisterForm, TaskForm
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
    count_taks = models.Task.objects.filter(user=request.user.id,active=True).count()
    data = (
        models.Form.objects.filter(active=True)
        .order_by("-priority","time")
        .select_related("implementer", "user")
        .prefetch_related("soimplementor")
    )
    return render(request, "watchdog.html", {"data": data,"tasks":count_taks})


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


@staff_member_required
def tasks(request):
    form = TaskForm()
    tasks = models.Task.objects.filter(user = request.user, active = True).order_by('-id')
    count_requests = models.Form.objects.filter(active = True).count()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid:
            task = form.save(commit=False)
            task.save()
            form = TaskForm
    return render(request,"tasks.html",{"form":form,"tasks":tasks,"requests":count_requests})

@require_POST
@staff_member_required
def taskdone(request,id):
    task = models.Task.objects.get(pk=id)
    if task.user == request.user:
        task.active = False
        task.save()
        return HttpResponse(200)
    else:
        return HttpResponse(403)


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
    req.save()
    return redirect("requests")


@require_POST
@staff_member_required
def sub_implementor(request, id):
    req = models.Form.objects.get(pk=id)
    if req.active == True:
        req.soimplementor.add(request.user)
    return redirect("requests")
