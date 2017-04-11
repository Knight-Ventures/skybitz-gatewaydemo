import config   #stores gateway credentials username/password - use generic creds in public shared project
import requests
import xmltodict
import json

class Gateway:
    '''Gateway class'''

    def __init__(self):
        '''Establish a gateway connection using a connection URL and auth credentials'''
        self.url = 'http://dev.tanklink.com/latlontdg_df/service.asmx?WSDL'

    def gatewayRequest(self, string):
        '''Make a request to the gateway web service with a specific soap envelope string'''
        #headers = {'content-type': 'application/soap+xml'}
        headers = {'content-type': 'text/xml'}
        response = requests.post(self.url, data=string, headers=headers)
        return str(response.content)

    def parseXML2dict(self, s):
        '''Parse the response xml string and create dictionary using xml2dict module'''

        begTagStr = '<soap:Body>'
        endTagStr = '</soap:Body>'
        bodyxml = s[s.find(begTagStr) : s.find(endTagStr) + len(endTagStr)]

        xmltodictoutput = xmltodict.parse(bodyxml)
        return xmltodictoutput

    def parseXML2json(self, d):
        '''Convert dict output from parseXML2dict to JSON'''
        j = json.dumps(d)
        return j

    def soapGetOrganization(self):
        '''Get the Org info'''
        uname = config.username
        pword = config.password
        soapEnv_GetOrganization = '''<soapenv:Envelope 
                                        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                                        xmlns:tem="http://tempuri.org/">
                                        <soapenv:Header/>
                                        <soapenv:Body>
                                            <tem:GetOrganization>
                                            <tem:iConsumerId>{0}</tem:iConsumerId>
                                            <!--Optional:-->
                                            <tem:sAuthentication>{1}</tem:sAuthentication>
                                            <tem:iNextID>0</tem:iNextID>
                                            </tem:GetOrganization>
                                        </soapenv:Body>
                                    </soapenv:Envelope>'''
        return soapEnv_GetOrganization.format(uname, pword)

    def soapGetLocation(self):
        '''Get the Location List array for the Org'''
        uname = config.username
        pword = config.password
        soapENV_GetLocation = '''<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
                                <soap:Header/>
                                <soap:Body>
                                    <tem:GetLocation>
                                        <tem:iConsumerId>{0}</tem:iConsumerId>
                                        <!--Optional:-->
                                        <tem:sAuthentication>{1}</tem:sAuthentication>
                                        <tem:iNextID>0</tem:iNextID>
                                    </tem:GetLocation>
                                </soap:Body>
                                </soap:Envelope>'''
        return soapENV_GetLocation.format(uname, pword)

    def soapGetTank(self):
        '''Get the Tank List array for the Org'''
        uname = config.username
        pword = config.password
        soapENV_GetTank = '''<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
                            <soap:Header/>
                            <soap:Body>
                                <tem:GetTank>
                                    <tem:iConsumerId>{0}</tem:iConsumerId>
                                    <!--Optional:-->
                                    <tem:sAuthentication>{1}</tem:sAuthentication>
                                    <tem:iNextID>0</tem:iNextID>
                                </tem:GetTank>
                            </soap:Body>
                            </soap:Envelope>'''
        return soapENV_GetTank.format(uname, pword)
