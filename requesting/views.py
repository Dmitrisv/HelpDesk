from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseForbidden
from datetime import datetime
from django.utils import timezone
from uuid import uuid4
from django.shortcuts import render
import plotly.graph_objects as go
import plotly.offline as opy
from datetime import datetime, timedelta
from django.views.generic import ListView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q


from . import models
from .forms import (
    AddrequestForm,
    RegisterForm,
    TaskForm,
    MessageForm,
    CustomUser,
    CustomChangePasswordForm,
)
from django.contrib.auth.models import Group


def create_plot(user):
    weekdays = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье",
    ]
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    data = {day: 0 for day in weekdays}
    forms = models.Form.objects.filter(
        user=user, created_at__gte=week_ago, created_at__lte=today
    )
    for form in forms:
        created_day = form.created_at.weekday()
        data[weekdays[created_day]] += 1
    days = list(data.keys())
    counts = list(data.values())
    fig = go.Figure(data=go.Bar(x=days, y=counts))
    fig.update_layout(
        xaxis_title="День недели",
        yaxis_title="Количество заявок",
    )
    div = opy.plot(fig, auto_open=False, output_type="div")
    return div


@login_required
def new_request(request):
    if request.method == "POST":
        form = AddrequestForm(request.POST, request.FILES)
        image_file = request.FILES.get("image")
        if image_file:
            image_file.name = f"{uuid4()}.png"
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form = AddrequestForm()
    else:
        form = AddrequestForm()
    return render(
        request,
        "req.html",
        {
            "form": form,
        },
    )


@staff_member_required
def get_all_requests(request):
    count_taks = models.Task.objects.filter(
        user=request.user.id, active=True
    ).count()
    data = (
        models.Form.objects.filter(active=True)
        .order_by("-priority", "time")
        .select_related("implementer", "user")
        .prefetch_related("soimplementor")
    )
    return render(request, "watchdog.html", {"data": data, "tasks": count_taks})


@login_required
def articles(request):
    query = request.GET.get("q")
    articles = models.Article.objects.values("title", "slug")

    if query:
        articles = articles.filter(Q(title__contains=query))
    return render(request, "articles.html", {"articles": articles})


@login_required
def get_article(request, article_slug):
    article = get_object_or_404(models.Article, slug=article_slug)
    return render(
        request,
        "article.html",
        {
            "article": article,
        },
    )


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("new")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name=form.cleaned_data["groups"])
            user.groups.add(group)
            login(request, user)
            return redirect("new")
    else:
        form = RegisterForm()
    return render(request, "registration/sign_up.html", {"form": form})


class HistoryListView(ListView):
    model = models.Form
    template_name = "history.html"
    context_object_name = "forms"
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by("-time")
        return queryset


@staff_member_required
def tasks(request):
    form = TaskForm()
    tasks = models.Task.objects.filter(user=request.user, active=True).order_by(
        "-id"
    )
    count_requests = models.Form.objects.filter(active=True).count()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid:
            task = form.save(commit=False)
            task.save()
            form = TaskForm
    return render(
        request,
        "tasks.html",
        {"form": form, "tasks": tasks, "requests": count_requests},
    )


@require_POST
@staff_member_required
def taskdone(request, id):
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
    req.done_at = timezone.make_aware(
        datetime.now(), timezone.get_default_timezone()
    )
    req.save()
    return redirect("requests")


@login_required
def profile(request):
    fig = create_plot(request.user)
    data = models.Form.objects.filter(user=request.user).order_by("-time")[:5]
    return render(request, "profile.html", {"reqs": data, "plot": fig})


@require_POST
@staff_member_required
def sub_implementor(request, id):
    req = models.Form.objects.get(pk=id)
    if req.active is True:
        req.soimplementor.add(request.user)
    return redirect("requests")


@login_required
def set_appearance(request):
    return render(request, "appearance_settings.html")


@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("change_password")
    else:
        form = CustomChangePasswordForm(request.user)

    return render(request, "security_settings.html", {"form": form})


class PublicProfileView(UpdateView):
    model = CustomUser
    fields = ["first_name", "last_name", "phone", "ip"]
    template_name = "profile_settings.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect("/settings/profile/")

    def get_object(
        self,
    ):
        return CustomUser.objects.get(pk=self.request.user.pk)


@login_required
def req_info(request, id):
    try:
        req = get_object_or_404(models.Form, pk=id)
        form = MessageForm()
        if request.user == req.user or request.user.is_staff is True:
            return render(
                request, "req_info.html", {"requests": req, "form": form}
            )
        else:
            raise HttpResponseForbidden
    except models.Form.DoesNotExist:
        raise Http404("404")
