from django.contrib import admin
from django.forms import ModelForm

from cards.models import Card


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = "__all__"

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    form = CardForm
    list_display = (Card.id.field.name, Card.owner.field.name, Card.created_at.field.name, Card.updated_at.field.name, Card.last_used_at.field.name)

