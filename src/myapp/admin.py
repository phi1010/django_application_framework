from uuid import uuid4

from django.contrib import admin
from django.forms import ModelForm
from django.forms.widgets import TextInput

from myproject.random_passwords import generate_password
from myapp.models import MyModel, RemoteClient
from myapp import door_names_publisher
from myapp import mqtt_dynsec


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

@admin.register(RemoteClient)
class RemoteClientAdmin(admin.ModelAdmin):
    form = RemoteClientForm
    list_display = (RemoteClient.username.field.name,)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields[RemoteClient.username.field.name].initial = uuid4()
        form.base_fields[RemoteClient.token.field.name].initial = generate_password()
        return form

    def save_model(self, request, obj, form, change):
        super(RemoteClientAdmin, self).save_model(request, obj, form, change)
        mqtt_dynsec.update_mqtt_client(obj)

    def delete_model(self, request, obj):
        super(RemoteClientAdmin, self).delete_model(request, obj)
        mqtt_dynsec.cleanup_all_clients_and_roles()

