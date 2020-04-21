import urllib3
import requests
import xmltodict
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings()


class AxSizzle(object):
    def __init__(self, ucm, timeout=10000, rejectUnauthorized=False):
        self.ucm = ucm
        self.soapXml = ''
        self.timeout = timeout
        self.rejectUnauthorized = rejectUnauthorized

    def buildRequest(self, method, body):
        self.soapXml = xmltodict.unparse({
            'SOAP-ENV:Envelope': {
                '@xmlns:SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/',
                '@xmlns:ns1': 'http://www.cisco.com/AXL/API/{}'.format(self.ucm['version']),
                'SOAP-ENV:Body': {
                    'ns1:{}'.format(method): body
                }
            }
        }, pretty=True)

    def callApi(self, message):
        self.buildRequest(message['method'], message['body'])
        try:
            response = requests.post(
                'https://{}:8443/axl/'.format(self.ucm['ip']),
                timeout=self.timeout,
                verify=self.rejectUnauthorized,
                headers={
                    'SOAPAction': 'CUCM:DB ver={} {}'.format(self.ucm['version'], message['method']),
                    'Content-Type': 'text/xml; charset=utf-8'
                },
                auth=HTTPBasicAuth(
                    self.ucm['username'], self.ucm['password']),
                data=self.soapXml
            )

            response.raise_for_status()

            return self.parseResponse(
                message['method'], response.text)

        except requests.exceptions.RequestException as err:
            return self.parseErrorResponse(err)

    def parseResponse(self, method, response):
        return xmltodict.parse(response)[
            'soapenv:Envelope']['soapenv:Body']['ns:{}Response'.format(method)]['return']

    def parseErrorResponse(self, message):
        return {'error': message}
