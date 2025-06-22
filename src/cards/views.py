from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


@login_required(login_url='/')  # TODO determine correct login URL
def home(request):
    messages.info(request, "Du hast lange nicht verwendete Karten. Bitte sperre oder lösche diese.")
    messages.error(request,
                   "Karte konnte nicht gelesen werden. Bitte Karte erneut an das Lesegerät halten und Aktion wiederholen.")
    context = dict(
        cards=request.user.cards.order_by("created_at").all(),
        messages=messages.get_messages(request),
    )
    return render(request, 'cards/index.html', context)



def register(request):
    return None

def disable_scan(request):
    return None


def modify(request, card_id):
    match request.POST.get("action"):
        case "delete":
            messages.warning(request, f"Karte {card_id} gelöscht.")
            pass
        case "disable":
            messages.success(request, f"Karte {card_id} gesperrt.")

    return redirect(home)