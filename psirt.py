#!/usr/bin/env python3
"""This script coordinatates the retrieval of the latest Cisco PSIRT

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

import configparser
import logging
from time import time
from os import path
from rich.console import Console
from rich.logging import RichHandler
from utils.otoken import otoken
from utils.psirts import latestpsirt

FIRST_RUN = True

console = Console()

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

log = logging.getLogger("rich")

config = configparser.ConfigParser()
config.read("config.ini")
grant = config["BEARER"]["grant_type"]
client_id = config["BEARER"]["client_id"]
client_secret = config["BEARER"]["client_secret"]

running_dir = path.join(path.dirname(__file__), "")

console.log(f"[bold cyan]--- Parent Directory: {running_dir} ---[/]")

if __name__ == "__main__":

    start_time = time()

    if FIRST_RUN is True:
        console.log("[bold cyan]--- Get Token ---[/]")
        access_token, token_type, token_expires = otoken(
            grant, client_id, client_secret
        )

    if start_time >= token_expires:
        console.log("[bold cyan]--- Refresh Token ---[/]")
        access_token, token_type, token_expires = otoken(
            grant, client_id, client_secret
        )

    latestpsirt(access_token)

    FIRST_RUN = False
