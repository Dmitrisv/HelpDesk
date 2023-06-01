from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from requesting.models import Form
from requesting.models import CustomUser as User
from django.db.models import Count
from datetime import date

import plotly.graph_objs as go
import plotly.offline as opy


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    workers = User.objects.filter(is_staff=True, is_superuser=False)
    workers_data = (
        Form.objects.filter(done_at__date=date.today(), implementer__in=workers)
        .values("implementer__last_name")
        .annotate(count=Count("id"))
    )

    workers_names = [
        worker["implementer__last_name"] for worker in workers_data
    ]
    counts = [worker["count"] for worker in workers_data]

    fig = go.Figure(data=[go.Bar(x=workers_names, y=counts, width=0.1)])

    fig.update_layout(
        title_text="Статистика на сегодня",
        title_font=dict(color="blue"),
        height=600,
        xaxis_title="Администраторы",
        yaxis_title="Количество заявок",
    )
    div = opy.plot(fig, auto_open=False, output_type="div")
    return render(request, "dashboard.html", {"plot": div})
