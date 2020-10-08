import logging
from time import sleep
from logging_splunk_hec import SplunkHecHandler

logger = logging.getLogger('SplunkHecHandler')
logger.setLevel(logging.DEBUG)

splunk_server = "splunkhec-test.com"
protocol = "https"
port = "8088"
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
    logger.warning("This is sample warning messages")
    logger.error("ERROR!! This is sample ERROR message")
    logger.debug("DEBUG!!, Sample Debug Message")
    sleep(5)
