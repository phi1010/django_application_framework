import ipaddress
import json
import logging
import time

from django.core import serializers
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from icecream import ic

from accounts.models import User
from myproject.opa import evaluate_policy
from django.conf import settings
from myapp.models import MyModel

log = logging.getLogger(__name__)



def home(request):
    user_models = list(mymodel for mymodel in MyModel.objects.all() if check_has_model_permission(request, mymodel, action="view"))
    user_models.sort(key=lambda d: d.order)
    context= dict(
        mymodels=user_models,
        messages=messages.get_messages(request),
    )
    return render(request, 'web_homepage/index.html', context=context)
    # return redirect("/...")




def check_has_model_permission(request,mymodel, action):
    user_dict = create_request_user_info(request)
    has_permission = evaluate_policy("app/myproject/authz/allow", dict(action="open",user=user_dict,door=serialize_model(mymodel)))
    return has_permission

def create_request_user_info(request):
    permissions = [serialize_model(perm) for perm in request.user.user_permissions.all()]
    if isinstance(request.user, User):
        user = serialize_model(request.user)
        user_connections = [serialize_model(conn) for conn in request.user.connections.all()]
    else:
        user = None
        user_connections = []
    authenticated = request.user.is_authenticated
    #ic(user_connections, permissions, user, authenticated, location_info)
    user_dict = dict(authenticated=authenticated, user=user, user_permissions=permissions,
                     user_connections=user_connections, )
    return user_dict


def serialize_model(model):
    model = json.loads(serializers.serialize('json', [model, ]))[0]
    if 'fields' in model and "password" in model['fields']:
        model['fields']['password'] = bool(model['fields']['password'])
    return model

