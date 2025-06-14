import ipaddress
import json
import logging
import os
import tarfile
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
    #ic(request, filename)
    # TODO auth
    match filename:
        case "door_authz.tar.gz":
            json_bytes = json.dumps(dict(foo=True, bar=False)).encode("utf8") + b"\n"
            rego_bytes = b"""
                package app.door_commander.physical_access
                
                default allow = false
            """
            def prepare_file(tar: tarfile.TarFile):
                # The filename data.json is ignored when loading the data file,
                # only the directories are used
                _add_file_to_tar(tar, "example/data.json", io.BytesIO(json_bytes))
                # For rego files, only the package declaration in the file is used.
                _add_file_to_tar(tar, "policy.rego", io.BytesIO(rego_bytes))

            #fd = open(path_to_file, 'rb')
            fd = _make_tarfile(prepare_file)
            file_name = filename.split("/")[-1]
            return _make_file_download_response(fd, file_name)
        case _:
            return HttpResponseNotFound()
    # return redirect("https://betreiberverein.de/impressum/")


def _make_tarfile(prepare_file):
    fd = io.BytesIO(b"")
    tar = tarfile.open(name=None, mode='w:gz', fileobj=fd)
    prepare_file(tar)
    tar.close()
    # ic(fd, fd.tell())
    # Seek to the start of the written tarfile
    fd.seek(0)
    return fd


def _make_file_download_response(fd, file_name):
    response = FileResponse(fd)
    response['Content-Disposition'] = 'inline; filename=' + file_name
    return response


def _add_file_to_tar(tar, filename, fd):
    tarinfo = tarfile.TarInfo(filename)
    fd.seek(0, os.SEEK_END)
    tarinfo.size = fd.tell()
    fd.seek(0)
    tar.addfile(tarinfo, fd)

