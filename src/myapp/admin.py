from uuid import uuid4

from django.contrib import admin
from django.forms import ModelForm
from django.forms.widgets import TextInput

from myproject.random_passwords import generate_password
from myapp.models import MyModel


class MyModelForm(ModelForm):
    class Meta:
        model = MyModel
        fields = "__all__"
        widgets = {
            "text_color": TextInput(attrs={"type": "color"}),
            "button_color": TextInput(attrs={"type": "color"}),
        }


@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    form = MyModelForm
    list_display = (MyModel.some_second_id.field.name, MyModel.display_name.field.name)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields[MyModel.some_second_id.field.name].initial = uuid4()
        return form

    def save_model(self, request, obj, form, change):
        super(MyModelAdmin, self).save_model(request, obj, form, change)
        # TODO trigger updates

