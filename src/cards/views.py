from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


@login_required(login_url='/') # TODO determine correct login URL
def home(request):
    messages.add_message(request, messages.INFO, "Hello world.")
    messages.debug(request, "%s SQL statements were executed." % 1)
    messages.info(request, "Three credits remain in your account.")
    messages.success(request, "Profile details updated.")
    messages.warning(request, "Your account expires in three days.")
    messages.error(request, "Document deleted.")
    return render(request, 'cards/index.html', {
        'title': 'Cards',
        'site_title': 'ZAM Door',
        'site_header': 'ZAM Door Commander',
    })