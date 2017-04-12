# soapreqs.py
import config  #stores gateway credentials username/password - use generic creds in public shared project

getorgenvtmp = '''<soapenv:Envelope 
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

getlocenvtmp = '''<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
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

gettankenvtmp = '''<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
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

def getOrgSoap():
    '''Returns the formatted soap xml request string for GetOrganization'''
    return getorgenvtmp.format(config.username, config.password)

def getLocSoap():
    '''Returns the formatted soap xml request string for GetLocation'''
    return getlocenvtmp.format(config.username, config.password)

def getTankSoap():
    '''Returns the formatted soap xml request string for GetTank'''
    return gettankenvtmp.format(config.username, config.password)
