import logging
import unittest
import time

from logging_splunk_hec import SplunkHecHandler

# These are intentionally different than the kwarg defaults
SPLUNK_PROTO = 'https'
SPLUNK_HOST = 'splunkhec-test.com'
SPLUNK_PORT = 8088
SPLUNK_TOKEN = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
CLIENT_HOSTNAME = 'Splunk-HEC-Test'
SPLUNK_SOURCE = ''
SPLUNK_SOURCETYPE = ''
SPLUNK_VERIFY = True

RECEIVER_URL = '%s://%s:%s/services/collector/event' % (
    SPLUNK_PROTO, SPLUNK_HOST, SPLUNK_PORT)


class TestSplunkHecHandler(unittest.TestCase):
    def setUp(self):
        self.splunk_handler = SplunkHecHandler(
            proto=SPLUNK_PROTO,
            host=SPLUNK_HOST,
            port=SPLUNK_PORT,
            token=SPLUNK_TOKEN,
            hostname=CLIENT_HOSTNAME,
            source=SPLUNK_SOURCE,
            sourcetype=SPLUNK_SOURCETYPE,
            ssl_verify=SPLUNK_VERIFY,
        )
        self.splunk_handler.testing = True

    def tearDown(self):
        self.splunk_handler = None

    def test_init(self):
        self.assertIsNotNone(self.splunk_handler)
        self.assertIsInstance(self.splunk_handler, SplunkHecHandler)
        self.assertIsInstance(self.splunk_handler, logging.Handler)
        self.assertEqual(self.splunk_handler.proto, SPLUNK_PROTO)
        self.assertIn(self.splunk_handler.proto, ['http', 'https'])
        self.assertEqual(self.splunk_handler.host, SPLUNK_HOST)
        self.assertEqual(self.splunk_handler.port, SPLUNK_PORT)
        self.assertIn(self.splunk_handler.port, range(0, 65535))
        self.assertEqual(self.splunk_handler.token, SPLUNK_TOKEN)
        self.assertEqual(self.splunk_handler.hostname, CLIENT_HOSTNAME)
        self.assertEqual(self.splunk_handler.source, SPLUNK_SOURCE)
        self.assertEqual(self.splunk_handler.sourcetype, SPLUNK_SOURCETYPE)
        self.assertEqual(self.splunk_handler.ssl_verify, SPLUNK_VERIFY)
        self.assertIsInstance(self.splunk_handler.ssl_verify, bool)


if __name__ == '__main__':
    unittest.main()
