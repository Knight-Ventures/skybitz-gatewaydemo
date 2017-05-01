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

getinvenvtmp = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetInventory>
         <tem:iConsumerId>{0}</tem:iConsumerId>
         <!--Optional:-->
         <tem:sAuthentication>{1}</tem:sAuthentication>
         <tem:iAckTransactionId>0</tem:iAckTransactionId>
      </tem:GetInventory>
   </soapenv:Body>
</soapenv:Envelope>'''

getinvalrmenvtmp = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetInventoryCalcAlarm>
         <tem:iConsumerId>{0}</tem:iConsumerId>
         <!--Optional:-->
         <tem:sAuthentication>{1}</tem:sAuthentication>
         <tem:iAckTransactionId>0</tem:iAckTransactionId>
      </tem:GetInventoryCalcAlarm>
   </soapenv:Body>
</soapenv:Envelope>'''

# NEW - this on is used to get the Inventory Alarm Calc with ACK code
getinvalrmenvtransact = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetInventoryCalcAlarm>
         <tem:iConsumerId>{0}</tem:iConsumerId>
         <!--Optional:-->
         <tem:sAuthentication>{1}</tem:sAuthentication>
         <tem:iAckTransactionId>{2}</tem:iAckTransactionId>
      </tem:GetInventoryCalcAlarm>
   </soapenv:Body>
</soapenv:Envelope>'''

gettankgenlatlonenv = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetTankGeneralLatLonPlus>
         <tem:iConsumerId>{0}</tem:iConsumerId>
         <!--Optional:-->
         <tem:sAuthentication>{1}</tem:sAuthentication>
         <tem:tankID>{2}</tem:tankID>
      </tem:GetTankGeneralLatLonPlus>
   </soapenv:Body>
</soapenv:Envelope>'''

def get_org_soap():
    '''Returns the formatted soap xml request string for GetOrganization'''
    return getorgenvtmp.format(config.username, config.password)

def get_loc_soap():
    '''Returns the formatted soap xml request string for GetLocation'''
    return getlocenvtmp.format(config.username, config.password)

def get_tank_soap():
    '''Returns the formatted soap xml request string for GetTank'''
    return gettankenvtmp.format(config.username, config.password)

def get_inv_soap():
    '''Returns the formatted soap xml request string for GetInventory'''
    return getinvenvtmp.format(config.username, config.password)

def get_invalrm_soap():
    '''Returns the formatted soap xml request string for GetInventory'''
    return getinvalrmenvtmp.format(config.username, config.password)

def get_tankgenlatlon_soap(tankidstr):
    '''Returns the formatted soap xml req string for GetTankGeneralLatLon
    Requires the TankID string as input.'''
    return gettankgenlatlonenv.format(config.username, config.password, tankidstr)

def get_invalrm_transactid_soap(transactidstr):
    '''Returns the formatted soap xml request string with a unique transactionID from previous request'''
    return getinvalrmenvtransact.format(config.username, config.password, transactidstr)
