# Cisco PSIRT Updates

This Python script connects to the Cisco PSIRT API and creates a CSV file in the reports folder of PSIRT updates that have occurred in the last 7 days.

## What problem is this script trying to solve?

Using the [Cisco Security Advisories portal](https://tools.cisco.com/security/center/publicationListing.x), it can be difficult to determine what PSIRT notifications have been updated with new information, affected products, workarounds, and patches.

This script utilizes the [Cisco PSIRT openVuln API](https://developer.cisco.com/docs/psirt/?utm_source=devblog&utm_medium=christophervandermade&utm_campaign=securex-page&utm_term=fy22-q2-0000&utm_content=log4j2andpsirt01-ww) to create a CSV file of all updated Cisco PSIRT notifications that have occurred in the last 7 days.

This CSV will make it easier for a security team to review updated PSIRT information and take any required remediatory actions.

## Cisco PSIRT OpenVuln API information

More information about the PSIRT OpenVuln API can be found on this [Cisco DevNet page](https://developer.cisco.com/psirt/).

## Requirements

This script requires a Python environment and the libraries included in the [requirements.txt](https://github.com/dirflash/psirt/blob/master/requirements.txt) file.

All the API keys are stored in a config.ini file using [configparser](https://docs.python.org/3/library/configparser.html). Your config.ini file should look like this:

![Sample config.ini file](https://github.com/dirflash/psirt/blob/master/images/config.jpg)

## Usage

```
$  python.exe psirt.py
```

[psirt.py](https://github.com/dirflash/psirt/blob/master/psirt.py) is the main script. It calls [otoken.py](https://github.com/dirflash/psirt/blob/master/utils/otoken.py) in the utils folder to obtain the OAuth Bearer access token. Then [psirts.py](https://github.com/dirflash/psirt/blob/master/utils/psirts.py) is called, using the Bearer token as authentication, all Cisco PSIRTs updated in the last 7 days are collected into a semi-colon delimited CSV file. The CSV file is created in the reports folder.

### Sample report

![This is a sample CSV report](https://github.com/dirflash/psirt/blob/master/images/sample_CSV.JPG)
