# Cisco PSIRT Updates

This Python script connects to the Cisco PSIRT API and creates a CSV file in the reports folder of PSIRT updates that have occurred in the last 7 days.

## Requirements

This script requires a Python environment and the libraries included in the [requirement.txt](https://github.com/dirflash/psirt/blob/master/requirements.txt) file.

## Usage

[psirt.py](https://github.com/dirflash/psirt/blob/master/psirt.py) is the main script. It calls [otoken.py](https://github.com/dirflash/psirt/blob/master/utils/otoken.py) in the utils folder to obtain the OAuth Bearer access token. Then [psirts.py](https://github.com/dirflash/psirt/blob/master/utils/psirts.py) is called, using the Bearer token as authentication, all Cisco PSIRTs updated in the last 7 days are collected into a semi-colon delimited CSV file. The CSV file is created in the reports folder.

### Sample report

![This is a sample CSV report](https://github.com/dirflash/psirt/blob/master/images/sample_CSV.JPG)
