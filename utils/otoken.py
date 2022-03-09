#!/usr/bin/env python3
"""This script obtains the authorization token to retrieve the latest Cisco PSIRT


__author__ = "Aaron Davis"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates"
__license__ = "CISCO SAMPLE CODE LICENSE"

Copyright (c) 2022 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied."""

import sys
from time import time
import requests
from rich import print  # pylint: disable=redefined-builtin
from rich.console import Console

console = Console()


def otoken(grant, client_id, client_secret):
    """This function creates the OAuth token

    Args:
        grant (str): Token grant type
            (https://raw.githubusercontent.com/api-at-cisco/Images/master/Token_Access.pdf)
        client_id (str): API username
        client_secret (str): API password

    Returns:
        access_token (str): Access token
        token_type (str): Token type ("Bearer")
        token_dies (time): When tocken expires
    """

    console.print("[dark_blue]Entered otoken function.[/]")

    url = (
        "https://cloudsso.cisco.com/as/token.oauth2?grant_type="
        + grant
        + "&client_id="
        + client_id
        + "&client_secret="
        + client_secret
    )

    payload = {}
    headers = {}

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.HTTPError:
        status = response.status_code
        if status == 401:
            print("[orange1]Invalid API key.[/]")
        elif status == 404:
            print("[orange1]Invalid input.[/]")
        elif status in (429, 443):
            print("[orange1]API calls per minute exceeded.[/]")
        sys.exit(1)

    data = response.json()

    access_token = data["access_token"]
    token_type = data["token_type"]
    token_expires = data["expires_in"]

    token_dies = time() + (token_expires - 120)

    console.print("[dark_blue]Exiting otoken function.[/]")

    return (access_token, token_type, token_dies)
