import ipaddress
import json
import logging
import os
import tarfile
import time
import io
import gzip

from django.core import serializers
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from icecream import ic

from door_commander import settings
from door_commander.opa import get_polices

log = logging.getLogger(__name__)


def get_bundle(request, filename: str):
    # ic(request, filename)
    if not _authorize_with_bearer(request):
        return HttpResponse('Unauthorized', status=401)
    match filename:
        case "door_authz.tar.gz":
            json_bytes = json.dumps(dict(foo=True, bar=False)).encode("utf8") + b"\n"

            def prepare_file(tar: tarfile.TarFile):
                policies = get_polices()
                for policy in policies:
                    # For rego files, only the package declaration in the file is used.
                    _add_file_to_tar(tar, policy.id, io.BytesIO(policy.raw.encode("utf8")))
                # The filename data.json is ignored when loading the data file,
                # only the directories are used
                _add_file_to_tar(tar, "example/data.json", io.BytesIO(json_bytes))

            # fd = open(path_to_file, 'rb')
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


# OPA calls this with POST, so CSRF protection needs to be disabled
@csrf_exempt
def post_decision_log(request: WSGIRequest, hostname):
    if not _authorize_with_bearer(request):
        return HttpResponse('Unauthorized', status=401)
    #ic(hostname, request.headers)
    body = request.body
    if request.headers.get("Content-Encoding") == "gzip":
        body = gzip.decompress(body)
    if not request.headers.get("Content-Type") == "application/json":
        raise Exception("Unsupported Content-Type")
    body = body.decode("utf-8")
    data = json.loads(body)
    for decision in data:
        #ic(decision)
        result = decision.get("result",None)
        input = decision.get("input",None)
        path = decision.get("path",None)
        timestamp = decision.get("timestamp",None)
        log.info(
            f"Decision logged by {hostname!r}:\n"
            f"Input= {input!r}\n"
            f"Path= {path!r}\n"
            f"Timestamp= {timestamp!r}\n"
            f"Result= {result!r}"
        )
    return HttpResponse("OK")


def _authorize_with_bearer(request: WSGIRequest):
    bearer = request.headers.get("Authorization", None)
    BEARER = "Bearer "
    if not bearer or not bearer.startswith(BEARER):
        return False
    token = bearer.lstrip(BEARER)
    # ic(token)
    authorized = settings.OPA_BUNDLE_SERVER_BEARER_TOKEN == token
    log.debug(
        f"Request from {request.META['REMOTE_ADDR']} to OPA bundles / decision log API was authorized: {authorized}")
    return authorized


# OPA calls this with POST, so CSRF protection needs to be disabled
@csrf_exempt
def post_status(request:WSGIRequest, hostname:str):
    if not _authorize_with_bearer(request):
        return HttpResponse('Unauthorized', status=401)
    # ic(hostname, request.headers)
    body = request.body
    if request.headers.get("Content-Encoding") == "gzip":
        body = gzip.decompress(body)
    if not request.headers.get("Content-Type") == "application/json":
        raise Exception("Unsupported Content-Type")
    body = body.decode("utf-8")
    data = json.loads(body)
    bundles_status = data.get("bundles", None)
    #decision_logs_status = data.get("decision_logs", None)
    version = data.get("labels", dict()).get("version", None)
    #ic(bundles_status, version)
    log.debug(f"On {hostname!r} bundle status: {bundles_status!r}")
    log.debug(f"On {hostname!r} version status: {version!r}")

    return HttpResponse("OK")