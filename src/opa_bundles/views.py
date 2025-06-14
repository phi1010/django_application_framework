import ipaddress
import json
import logging
import time
import io

from django.core import serializers
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponseNotFound
from django.contrib import messages
from django.views.decorators.http import require_POST
from icecream import ic

log = logging.getLogger(__name__)


def get_bundle(request, filename:str):
    ic(request, filename)
    match filename:
        case "door_authz.tar.gz":
            #fd = open(path_to_file, 'rb')
            fd = io.BytesIO(b"some initial binary data: \x00\x01")
            response = FileResponse(fd)
            file_name = filename.split("/")[-1]
            response['Content-Disposition'] = 'inline; filename=' + file_name
            return response
        case _:
            return HttpResponseNotFound()
    # return redirect("https://betreiberverein.de/impressum/")

