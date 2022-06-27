#!/usr/bin/python3

# DISCLAIMER:
"""
This script is for demo purposes only which provides customers with programming information regarding the Developer APIs. This script is supplied "AS IS" without any warranties and support.

We assume no responsibility or liability for the use of the script, convey no license or title under any patent or copyright.

We reserve the right to make changes in the script without notification and make no representation or warranty that such application will be suitable for the specified use without further testing or modification.

"""

from datadog import initialize, statsd
import requests, json, os
from akamai.edgegrid import EdgeGridAuth,EdgeRc
from urllib.parse import urljoin
from datetime import datetime, timedelta
import logging
import json_log_formatter

# Initialize the authorization parameters for the API calls
def config_init():
    rc_path = os.path.expanduser('~/.edgerc')
    edgerc = EdgeRc(rc_path)
    global baseurl
    baseurl = 'https://%s' % edgerc.get('default', 'host')

    global session
    session = requests.Session()
    session.auth = EdgeGridAuth.from_edgerc(edgerc, 'default')


# MAIN PROGRAM
if __name__ == "__main__":

    options = {
        'statsd_host':'127.0.0.1',
        'statsd_port':8125,
        'statsd_namespace':'akamai'
    }

    initialize(**options)

    # Main Function
    config_init()
    cpcodes = ["01234"]
    dimensions = "600"
    metrics = "617,619,620,630,631"

    starttime = (datetime.now() - timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M")
    endtime = (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M")

    # Enable Logging. DD agent configured to read from the file defined below.
    formatter = json_log_formatter.JSONFormatter()

    json_handler = logging.FileHandler(filename='/var/log/akamai-media-reporting-log.json')
    json_handler.setFormatter(formatter)

    logger = logging.getLogger('my_json')
    logger.addHandler(json_handler)
    logger.setLevel(logging.INFO)

    for cpcode in  cpcodes:
        # Akamai Media Report API
        # 617 - 2xx
        # 619 - 4xx
        # 620 - 5xx
        # 630 - All Edge Hits
        # 631 - All Origin Hits
        api_call = urljoin(baseurl, '/media-delivery-reports/v1/adaptive-media-delivery/realtime-data?'+ 'startDate=' + starttime + 'Z&endDate=' + endtime + 'Z&' + 'cpcodes=' + cpcode + '&limit=1000&offset=0&dimensions=' + dimensions + '&metrics=' + metrics + '&aggregation=300')

        print("Sending API call: ", api_call)
        response = session.get(api_call, timeout=20)

        print("API call response status code: ", response.status_code)
        print("API call response: ", json.dumps(response.json(), indent=4, sort_keys=True))
        response_dict = json.loads(response.text)

        # Log
        logger.info(json.dumps(response.json()), extra={'cpcode': cpcode})

        # Collect the metrics only if the status code is 2xx
        if 200 <= response.status_code < 300:
            print("Found Metrics in API Response: ", response_dict['columns'][1]['aggregate'], response_dict['columns'][2]['aggregate'], response_dict['columns'][3]['aggregate'], response_dict['columns'][4]['aggregate'], response_dict['columns'][5]['aggregate'])

            # Metrics
            statsd.increment('2xxEdgeHits', float(response_dict['columns'][1]['aggregate']))
            statsd.increment('4xxEdgeHits', float(response_dict['columns'][2]['aggregate']))
            statsd.increment('5xxEdgeHits', float(response_dict['columns'][3]['aggregate']))
            statsd.increment('allEdgeHits', int(response_dict['columns'][4]['aggregate']))
            statsd.increment('allOriginHits', int(response_dict['columns'][5]['aggregate']))