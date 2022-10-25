#!/usr/bin/env python3

import json, requests
from requests.exceptions import ConnectionError

def replace_dicts ( obj, rep_str, payload ):
    new_obj = {}
    # Replaces each replace-string ('i.e. PAYLOAD') in all dict keys' values with the payload.
    for key, value in obj.items():
        new_val = value.replace( rep_str, payload )
        new_obj[key] = new_val
    return new_obj

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
    # Making copy so as not to overwrite actual endpoint object
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
    proxies=proxies,
    )

    except (ConnectionError, UnboundLocalError):
        print("[!]FATAL: Host does not exist or cannot be reached.")
        exit()


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
