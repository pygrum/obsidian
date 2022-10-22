#!/usr/bin/env python3
import processor, argparse, json

import json, requests

def log ( call ):
    """
    This function will send a json object of the details of the request that we sent, as well as the details of
    the response of the server. This is for the future, to export data to a dashboard for example.
    """
    print(call)

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



