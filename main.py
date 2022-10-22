#!/usr/bin/env python3
import processor, argparse, json

import json, requests

def log ( call ):
    """
    This function will send a json object of the details of the request that we sent, as well as the details of
    the response of the server. This is for the future, to export data to a dashboard for example.
    """
    print(call)




def start (target_file, payload_file, args):

    """
    starts processing combinations of targets, payloads and endpoints
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
    response = requests.request(
    REQUEST_VERB,                               # e.g. get, post, put, delete
    URL,                                    
    params=PARAMS,                              # get request parameters (empty dict if nonexistent)
    headers=HEADERS,                            
    cookies=COOKIES,
    json=JSON,                                  # json in request body
    data=DATA, 
    proxies=proxies                                 # any post data (file input support can be added in the future)
    )


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
    log(call)

    


def load_jsons (target_file, payload_file):
    with open(target_file, "r") as tf:
        target_data = json.load(tf)                             # Convert json file into dictionary named 'targets'

    with open(payload_file, "r") as pf:
        payloads = json.load(pf)                            # Convert json file to array of dicts, named 'payload_data'

    replace_string = target_data["replace-string"]
    proxies = target_data["proxies"]
    for target in target_data["targets"]:
        for endpoint in target["endpoints"]:
            for payload in payloads:
                if ((payload["id"] in args.fp) or (target["id"] in args.ft)) or ((args.fp == []) and (args.ft == [])):
                    call = processor.process(target, payload, endpoint, replace_string, proxies)
                    log (call)       # payloads|>----endpoint|>----target
                else:
                    continue



parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

run = subparsers.add_parser("run")
run.add_argument("--targets", metavar="", default="targets.json", help="specify json file full of targets (use targets.json as writing reference)")
run.add_argument("--payloads", metavar="", default="payloads.json", help="specify json file full of payloads (use payloads.json as writing reference)")
run.add_argument("-fp", metavar="",nargs="*", default=[], help="run payloads that match the IDs specified")
run.add_argument("-ft", metavar="",nargs="*", default=[], help="test against targets that match the IDs specified")

args = parser.parse_args()
start(args.targets, args.payloads, args)



