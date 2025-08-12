from datetime import datetime, timedelta, UTC

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
import logging

from wait_until import wait_until

log = logging.getLogger(__name__)


@login_required(login_url='/')  # TODO determine correct login URL
def home(request):

    context = dict(
        messages=messages.get_messages(request),
    )
    return render(request, 'cards/index.html', context)

