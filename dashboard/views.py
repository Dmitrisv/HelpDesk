from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test

from requesting.models import Form
from requesting.models import CustomUser as User
from datetime import date

import plotly.graph_objs as go
import plotly.offline as opy

@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    data = []
    workersid = User.objects.filter(is_staff=True,is_superuser=False,).values_list("id",flat=True)
    workersusername = User.objects.filter(is_staff=True,is_superuser=False).values_list("last_name",flat=True)
    for i in workersid:
        data.append(Form.objects.filter(Q(done_at__date=date.today()),implementer = i).count())
    fig = go.Figure(data=[go.Bar(y=data,x=list(workersusername),width=[0.1])])
    fig.update_layout(
        title_text='Статистика на сегодня',
        title_font = dict(color='blue'),
        height=600     
        )
    div = opy.plot(fig, auto_open=False, output_type='div')
    return render(request, 'dashboard.html', {'plot': div})

