from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


@login_required(login_url='/') # TODO determine correct login URL
def home(request):
    messages.info(request, "Du hast lange nicht verwendete Karten. Bitte sperre oder lösche diese.")
    messages.success(request, "Karte gesperrt.")
    messages.warning(request, "Karte gelöscht.")
    messages.error(request, "Karte konnte nicht gelesen werden. Bitte Karte erneut an das Lesegerät halten und Aktion wiederholen.")
    context = dict(title='Cards', site_title='ZAM Door', site_header='ZAM Door Commander',
                   messages=messages.get_messages(request),
                   )
    return render(request, 'cards/index.html', context)