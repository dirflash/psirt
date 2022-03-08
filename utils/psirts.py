#!/usr/bin/env python3
"""This script retrieves and creates a CSV of Cisco PSIRT's updated in the last 7-days"""

import sys
import csv
import json
from datetime import date, timedelta
import requests
from rich import print, box  # pylint: disable=redefined-builtin, unused-import
from rich.console import Console

console = Console()
DEBUG = False
TODAY = date.today()
TODAY_STR = str(TODAY)
DELTA = timedelta(days=90)
NINTY_DAYS = TODAY - DELTA
NINTY_DAYS_STR = str(NINTY_DAYS)


def recent_update(verify_cve_date):
    """Determines if CVE entry has been updated in last 7 days

    Args:
        verify_cve_date (string): yyyy-mm-ddThh:mm:ss

    Returns:
        bool: True if entry has been updated in last 7 days
    """
    t_index = verify_cve_date.index("T")
    stripped_date = verify_cve_date[:t_index:]
    split_date = tuple(stripped_date.split("-"))
    new_date = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
    seven_days = date.today() - timedelta(days=7)
    recent = seven_days < new_date
    return recent


def latestpsirt(access_token):  # pylint: disable=too-many-locals
    """Obtains the following information from the latest PSIRT:
            - Advisory ID
            - Advisory Title
            - CVE's
            - CVE Base Score
            - Criticality [SIR (Security Impact Rating (critical, high, medium, low))]
            - PSIRT Version
            - First Published
            - Last Updated
            - Status (Final, Interim)
            - Products
            - Public URL

    Args:
        access_token (str): token required to access PSIRT information
    """

    console.print("[dark_blue]Entered latest PSIRT function.[/]")

    url = (
        "https://api.cisco.com/security/advisories/all/firstpublished?startDate="
        + NINTY_DAYS_STR
        + "&endDate="
        + TODAY_STR
    )

    beartoken = "Bearer " + access_token

    payload = {}
    headers = {"Authorization": beartoken}

    try:
        console.log("[dark_blue]Getting PSIRTs[/]")
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.HTTPError:
        status = response.status_code
        if status == 401:
            console.log("[orange1]Invalid API key.[/]")
        elif status == 404:
            console.log("[orange1]Invalid input.[/]")
        elif status in (429, 443):
            console.log("[orange1]API calls per minute exceeded.[/]")
        sys.exit(1)

    json_response = json.loads(response.text)

    cve_entries = json_response["advisories"]

    entry_count = 1
    updated_entries = 0

    header_names = [
        "Advisory_ID",
        "Advisory_Title",
        "CVE_Base_Score",
        "Criticality",
        "PSIRT_Version",
        "First_Published",
        "Last_Updated",
        "CVE_Status",
        "Products",
        "Pub_URL",
    ]

    with open(
        r".\reports\Cisco_PSIRT_" + TODAY_STR + ".csv",
        "w",
        newline="",
        encoding="UTF-8",
    ) as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=";")
        csvwriter.writerow(header_names)

        for entry in cve_entries:
            last_updated = entry["lastUpdated"]
            fresh_update = recent_update(last_updated)
            if fresh_update is True:
                updated_entries += 1
                advisory_id = entry["advisoryId"]
                advisory_title = entry["advisoryTitle"]
                cve_score = entry["cvssBaseScore"]
                criticality = entry["sir"]
                psirt_version = entry["version"]
                first_published = entry["firstPublished"]
                cve_status = entry["status"]
                product_names = entry["productNames"]
                pub_url = entry["publicationUrl"]
                row = [
                    advisory_id,
                    advisory_title,
                    cve_score,
                    criticality,
                    psirt_version,
                    first_published,
                    last_updated,
                    cve_status,
                    product_names,
                    pub_url,
                ]
                csvwriter.writerow(row)

            entry_count += 1

    console.log(f"[dark_blue]Total number of CVE entries: [bold]{entry_count}[/]")
    console.log(f"[dark_blue]Number of updated CVE entries: [bold]{updated_entries}[/]")

    console.log("[dark_blue]Exit get PSIRTs function.[/]")
