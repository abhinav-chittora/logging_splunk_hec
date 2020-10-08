import json
import logging
import time
import requests
import ast
import socket


class SplunkHecHandler(logging.Handler):
    URL_PATTERN = "{0}://{1}:{2}/services/collector"
    TIMEOUT = 30

    def __init__(self, host, token, **kwargs):
        self.host = host
        self.token = token
        if kwargs is not None:
            self.port = int(kwargs.get('port', 443))
            self.proto = kwargs.get('proto', 'https')
            self.ssl_verify = False if (kwargs.get('ssl_verify') in ["0", 0, "false", "False", False]) \
                else kwargs.get('cert') or True
            self.source = kwargs.get('source')
            self.index = kwargs.get('index')
            self.sourcetype = kwargs.get('sourcetype')
            self.hostname = kwargs.get('hostname', socket.gethostname())
            self.endpoint = kwargs.get('endpoint', '')
        try:
            s = socket.socket()
            s.settimeout(kwargs.get('timeout', self.TIMEOUT))
            s.connect((self.host, self.port))

            # Socket accessible.  Establish requests session
            self.r = requests.session()
            self.r.max_redirects = 1
            self.r.verify = self.ssl_verify
            self.r.headers['Authorization'] = "Splunk {}".format(self.token)
            logging.Handler.__init__(self)
        except Exception as err:
            logging.debug("Failed to connect to remote Splunk server (%s:%s). Exception: %s" % (
                self.host, self.port, err))
            raise err
        else:
            self.url = self.URL_PATTERN.format(
                self.proto, self.host, self.port, self.endpoint)
            s.close()

    def emit(self, record):
        body = {'log_level': record.levelname}
        try:
            if record.msg.__class__ == dict:
                body.update(record.msg)
            else:
                body.update({'message': ast.literal_eval(str(record.msg))})
        except Exception as err:
            logging.debug(
                "Log record sending exception raised. Exception: %s " % err)
            body.update({'message': record.msg})

        event = dict({'host': self.hostname, 'event': body})
        # For Splunk Version 7.x+, removing empty message
        if self.source is not None:
            event['source'] = self.source

        if self.sourcetype is not None:
            event['sourcetype'] = self.sourcetype

        if self.index is not None:
            event['index'] = self.index

        # Use timestamp from event if available
        if 'time' in body.keys():
            event['time'] = body['time']
        # Resort to current time
        else:
            event['time'] = int(time.time())
        if ('message' in body.keys()):
            try:
                for k, v in body['message'].items():
                    if k in ['host', 'source', 'sourcetype', 'time', 'index']:
                        event[k] = v
                    else:
                        try:
                            if type(v) in [str, list]:
                                event['message'][k] = v
                            else:
                                event['message'][k] = str(v)
                        except Exception:
                            pass
            except Exception:
                pass
        else:
            body.pop('message')

        try:
            data = json.dumps(event, sort_keys=True,
                              skipkeys=True, default=self.serializer)
        except TypeError:
            raise

        # Sending the events to Splunk
        try:
            req = self.r.post(self.url, data=data, timeout=self.TIMEOUT, headers={
                'Connection': 'close'})
            req.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.debug("Failed to emit record to Splunk server (%s:%s).  Exception raised: %s"
                          % (self.host, self.port, err))
            raise err

    @ staticmethod
    def serializer(obj):
        if type(obj) in [set, frozenset, range]:
            return list(obj)
        else:
            try:
                return str(obj)
            except Exception:
                raise
