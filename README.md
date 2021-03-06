# logging_splunk_hec

Python module for sending events to Splunk HEC

## Installation

```shell
pip install logging_splunk_hec
```

## Features

- Log message to Splunk HEC (HTTP Event Collector) directly.
- All messages are send as JSON sourcetype by default. If no time is available in events, current timestamp is used.
- If normal text message is passed, a directory is created with log_level and messages

![simple message logging](https://github.com/abhinav-chittora/logging_splunk_hec/blob/main/images/simple.png)

- If JSON dictonary is passed as messages, the  dictonary object is preserved.

![dictonary message logging](https://github.com/abhinav-chittora/logging_splunk_hec/blob/main/images/dict.png)

## Sample Code

```python
import logging
from time import sleep
from logging_splunk_hec import SplunkHecHandler

logger = logging.getLogger('SplunkHecHandler')
logger.setLevel(logging.DEBUG)

splunk_server = "splunkhec-test.com"
protocol = "https"
port = "443"
token = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
splunk_handler = SplunkHecHandler(splunk_server,
                                  token,
                                  port=port, proto=protocol, ssl_verify=True,
                                  sourcetype="_json")

logger.addHandler(splunk_handler)

for i in range(1, 3):
    dict_obj = {'message': {'eventnumber': i, 'api_endpoint': 'test_endpoint'},
                'user': 'abhinav', 'app': 'my demo app', 'severity': 'low'}
    logger.info(dict_obj)
    logger.warn("This is sample warning messages")
    logger.error("ERROR!! This is sample ERROR message")
    logger.debug("DEBUG!!, Sample Debug Message")
    sleep(5)
```
