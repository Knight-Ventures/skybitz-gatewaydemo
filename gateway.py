import requests
import xmltodict
import json

class Gateway:
    '''Gateway class'''

    def __init__(self):
        '''Establish a gateway connection using a connection URL and auth credentials'''
        self.url = 'http://dev.tanklink.com/latlontdg_df/service.asmx?WSDL'

    def gatewayRequest(self, string):
        '''Make a request to the gateway web service with a specific soap envelope string.
        Returns soap response string'''
        headers = {'content-type': 'text/xml'}
        #headers = {'content-type': 'application/soap+xml'}
        try:
            response = requests.post(self.url, data=string, headers=headers)
            return str(response.content)
        except:
            return 'gateway request error'

    def parseResponse(self, s):
        '''Parse the response xml string and create dictionary using xmltodict module.
        Returns ordered dictionary of the xml response starting the soap:Body node'''
        begTagStr = '<soap:Body>'
        endTagStr = '</soap:Body>'
        try:
            bodyxml = s[s.find(begTagStr) : s.find(endTagStr) + len(endTagStr)]
            return xmltodict.parse(bodyxml)
        except:
            bodyxml = {'error':'parse error'}
            return bodyxml

    def parseDisctionary(self, d):
        '''Convert dict output from parseResponse to JSON. 
        Returns json formatted string'''
        # return json.dumps(d)
        return json.dumps(d, sort_keys=True, indent=4)
