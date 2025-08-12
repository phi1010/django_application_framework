import logging
import urllib.parse
from dataclasses import dataclass

import requests
from icecream import ic
from django.conf import settings

log = logging.getLogger(__name__)

@dataclass
class Policy:
    id:str
    raw:str
    def __repr__(self):
        return f"Policy(id={self.id!r}, raw={self.raw[:100]!r}...)"

def get_polices():
    try:
        url = settings.OPA_URL
        token = settings.OPA_BEARER_TOKEN
        response = requests.get(url + "/v1/policies", headers=get_auth_header())

        if response.status_code != 200:
            raise Exception("Querying OPA failed")

        result_wrapper = response.json()
        result = result_wrapper["result"]
        policies = [Policy(item["id"], item["raw"]) for item in result]
        log.debug(f"Loaded policies: {policies}")
        return policies
    except Exception as e:
        raise Exception(f"OPA query failed: {e}") from e

def evaluate_query(query, input):
    # TODO test this.
    try:
        url = settings.OPA_URL
        payload = dict(input=input, query=query)
        response = requests.post(url + "/v1/query", json=payload, headers=get_auth_header())

        if response.status_code != 200:
            raise Exception("Auth failed")

        result_wrapper = response.json()
        result = result_wrapper["result"]
        return result
    except Exception as e:
        raise Exception(f"OPA query failed: {e}") from e


def get_auth_header():
    return dict(Authorization="Bearer " + settings.OPA_BEARER_TOKEN)


def evaluate_policy(path, input):
    return get_data_result(path, input) is True

def check_allowed(path, input):
    if get_data_result(path+"/allow", input) is True:
        return
    else:
        raise Exception("Unauthorized")  # TODO 401/403

def get_data_result(path, input):
    """

    :param path: might be "system/authz/allow"
    :param function:
    :return:
    """
    try:
        url = settings.OPA_URL
        token = settings.OPA_BEARER_TOKEN
        input = dict(input=input)
        # Normalize the URL, OPA uses problematic redirects https://github.com/open-policy-agent/opa/issues/2137
        url: str
        fullurl = url \
                  + ("" if url.endswith("/") else "/") \
                  + "v1/data" \
                  + ("" if path.startswith("/") else "/") \
                  + path
        response = requests.post(fullurl, json=input, headers=get_auth_header())

        if response.status_code != 200:
            raise Exception("OPA query failed")

        result = response.json()
        # log.setLevel(logging.DEBUG)
        log.debug("Return authorization result %s", ic.format(path, input, result))
        return result['result'] if 'result' in result else None
    except Exception as e:
        raise Exception(f"OPA query failed: {e}")

