#!/usr/bin/env python3
"""This script coordinatates the retrieval of the latest Cisco PSIRT"""

__author__ = "Aaron Davis"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2021 Aaron Davis"
__license__ = "MIT License"

import configparser
import logging
from time import time  # , sleep
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
