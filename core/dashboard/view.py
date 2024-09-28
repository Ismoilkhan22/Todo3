from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from base.helper import counter, user_home


@login_required(login_url='login')
def index(request):

    return render(request, 'pages/index.html', {'count': counter(request.user.id)})




