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

