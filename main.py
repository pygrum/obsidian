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

def log ( call ):
    """
    This function will send a json object of the details of the request that we sent, as well as the details of
    the response of the server. This is for the future, to export data to a dashboard for example.
    """
    # print( call )



def replace_dicts ( obj, rep_str, payload ):
    # Replaces each replace-string ('i.e. PAYLOAD') in all dict keys' values with the payload.
    for key, value in obj.items():
        value = value.replace( rep_str, payload )
        obj[key] = value
    return obj

def process (target, payload, endpoint, rep_str): 
    """
    This function constructs the request based off of the values defined in the targets file.
    """

    # Next block defines the request details
    # and replaces wherever the payload replace string ('i.e. PAYLOAD') is with the actual payload

    REQUEST_VERB = endpoint["method"]
    URL = target["uri"] + endpoint["endpoint"]

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
    response = requests.request(
    REQUEST_VERB,                               # e.g. get, post, put, delete
    URL,                                    
    params=PARAMS,                              # get request parameters (empty dict if nonexistent)
    headers=HEADERS,                            
    cookies=COOKIES,
    json=JSON,                                  # json in request body
    data=DATA,                                  # any post data (file input support can be added in the future)
    )


    call = {
        "method":REQUEST_VERB,
        "url":URL,
        "params":PARAMS,
        "headers":HEADERS,
        "cookies":COOKIES,
        "post-data":{
            "json":JSON,
            "data":DATA,
        },
        "status-code":response.status_code
        "response-data":response.__dict__
    }
    log(call)

    


def load_jsons (target_file, payload_file):
    with open(target_file, "r") as tf:
        target_data = json.load(tf)                             # Convert json file into dictionary named 'targets'

    with open(payload_file, "r") as pf:
        payloads = json.load(pf)                            # Convert json file to array of dicts, named 'payload_data'

    replace_string = target_data["replace-string"]
    for target in target_data["targets"]:
        for endpoint in target["endpoints"]:
            for payload in payloads:
                process(target, payload, endpoint, replace_string)        # payloads|>----endpoint|>----target



if __name__ == "__main__":
    load_jsons("targets.json", "payloads.json")

