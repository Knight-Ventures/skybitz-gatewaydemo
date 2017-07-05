import requests
import xmltodict
import json
import os

class Gateway:
    '''Gateway class'''

    def __init__(self):
        '''Establish a gateway connection using a connection URL and auth credentials'''
        self.url = 'http://dev.tanklink.com/latlontdg/service.asmx?WSDL'

    def gateway_request(self, string):
        '''Make a request to the gateway web service with a specific soap envelope string.
        Returns soap response string'''
        headers = {'content-type': 'text/xml'}
        #headers = {'content-type': 'application/soap+xml'}
        try:
            response = requests.post(self.url, data=string, headers=headers)
            return str(response.content)
        except:
            return 'gateway request error'

    def parse_response(self, respinput):
        '''Parse the response xml string and create dictionary using xmltodict module.
        Returns ordered dictionary of the xml response starting the soap:Body node'''
        beg_tag_str = '<soap:Body>'
        end_tag_str = '</soap:Body>'
        try:
            xmldict = respinput[respinput.find(beg_tag_str) : respinput.find(end_tag_str) + len(end_tag_str)]
            return xmltodict.parse(xmldict)
        except:
            xmldict = {'error':'parse error'}
            return xmldict

    def parse_dictionary(self, pdinput):
        '''Convert dict output from parseResponse to JSON.
        Returns json formatted string'''
        # return json.dumps(pdinput)
        return json.dumps(pdinput, sort_keys=True, indent=4)

    def save_resp_json(self, resp):
        '''Save the dictionary formatted response from parseResponse to local JSON file.
        Returns bool status of json file write'''
        try:
            #create json filename from root key, overwrite if exists
            file = ''
            for k in resp['soap:Body']:
                file = 'data/' + str(k) + '.json'
                break
            writefile = open(file, 'w')
            writefile.write(json.dumps(resp, sort_keys=True, indent=4))
            return True
        except FileNotFoundError:
            return False

    def save_resp_unique_json(self, resp, uniqueid):
        '''Save the dictionary formatted response from parseResponse to local JSON file.
        This is a unique json file which includes an id in filename
        Returns bool status of json file write'''
        try:
            #create json filename from root key, overwrite if exists
            file = ''
            for k in resp['soap:Body']:
                file = 'data/' + str(k) + uniqueid + '.json'
                break
            writefile = open(file, 'w')
            writefile.write(json.dumps(resp, sort_keys=True, indent=4))
            return True
        except FileNotFoundError:
            return False

    def delete_resp_unique_json(self, delfile):
        '''Delete the local JSON file.
        Used to clean up json files or to remove any with no records.
        Returns bool status of json file delete'''
        try:
            os.remove(delfile)
            return True
        except FileNotFoundError:
            return False

    def test_connect(self):
        '''Simple test to make sure the gateway is up and running. 
        Returns true if OK'''
        #TODO: Need to complete this
        return True

class Process():
    '''Process class for processing data in JSON obtained from Gateway'''

    def __init__(self):
        '''Create process for reading data from json'''
        self.tankjsonfile = 'data/GetTankResponse.json'
        self.inventoryfile = 'data/GetInventoryResponse.json'
        self.tankgenlatlonplus = 'data/GetTankGeneralLatLonPlusResponse{0}.json'
        self.invcalcalrmfile = 'data/GetInventoryCalcAlarmResponse.json'
        self.invcalcalrmfilelatest = 'data/GetInventoryCalcAlarmResponse_latest.json'
        self.uniqueinvcalcalrmfile = 'data/GetInventoryCalcAlarmResponse{0}.json'

    def get_json_file(self, filestring):
        '''Get the dictionary of tanks from JSON file. Takes filestring name
        Returns a dict'''
        try:
            openfile = open(filestring, 'r')
            jsonfiledict = json.loads(openfile.read())
        except FileNotFoundError:
            jsonfiledict = '{ }'  #if not found, return empty dict
        return jsonfiledict

    def get_tank_list(self):
        '''Get tank list. Returns list of tank IDs'''
        jsonfromfile = self.get_json_file(self.tankjsonfile)

        returnlist = []
        #check for key error
        try:
            listfromjson = jsonfromfile['soap:Body']['GetTankResponse']['GetTankResult']['Tank'] #returns list
            for k in listfromjson:
                if k['iTankID']:
                    returnlist.append(k['iTankID'])
        except KeyError:
            pass
            #log key error, ignore?
        return returnlist

    def get_inventorycalcalrm_transactID(self):
        '''Get inventory calc alarm. Returns only the TransactionID string'''
        jsonfromfile = self.get_json_file(self.invcalcalrmfile)

        transactIDfromjson = ''
        #check for key error
        try:
            transactIDfromjson = jsonfromfile['soap:Body']['GetInventoryCalcAlarmResponse']['iTransactionId'] #returns string value
        except KeyError:
            pass
            #log key error, ignore?
        return transactIDfromjson

    def get_inventorycalcalrm_unique_transactID(self, prevtransactid):
        '''Get UNIQUE inventory calc alarm. Returns only the unique TransactionID string'''
        jsonfromfile = self.get_json_file(self.uniqueinvcalcalrmfile.format(prevtransactid))

        uniquetransactIDfromjson = ''
        #check for key error
        try:
            uniquetransactIDfromjson = jsonfromfile['soap:Body']['GetInventoryCalcAlarmResponse']['iTransactionId'] #returns string value
        except KeyError:
            pass
            #log key error, ignore?
        return uniquetransactIDfromjson

    def count_inventorycalcalrm(self):
        '''Get inventory calc alarm list. Returns a count of the items in the list as an int'''
        jsonfromfile = self.get_json_file(self.invcalcalrmfile)
        listcount = 0
        try:
            listfromjson = jsonfromfile['soap:Body']['GetInventoryCalcAlarmResponse']['GetInventoryCalcAlarmResult']['CalcAlarmInventory'] #returns list
            for k in listfromjson:
                if k['iInventoryID']:
                    listcount += 1
        except KeyError:
            pass
            #log key error, ignore?
        return listcount
    
    def count_inventorycalcalrmlatest(self):
        '''Get inventory calc alarm list from latest file. Returns a count of the items in the list as an int'''
        jsonfromfile = self.get_json_file(self.invcalcalrmfilelatest)
        listcount = 0
        try:
            listfromjson = jsonfromfile['soap:Body']['GetInventoryCalcAlarmResponse']['GetInventoryCalcAlarmResult']['CalcAlarmInventory'] #returns list
            for k in listfromjson:
                if k['iInventoryID']:
                    listcount += 1
        except KeyError:
            pass
            #log key error, ignore?
        return listcount

    def count_inventorycalcalrm_unique(self, prevtransactid):
        '''Get UNIQUE inventory calc alarm list. Returns a count of the items in the unique list as an int'''
        jsonfromfile = self.get_json_file(self.uniqueinvcalcalrmfile.format(prevtransactid))
        #Fixed to only count if valid data for each list element (ie. not xsi:nil)
        # listcount = 0
        # try:
        #     listfromjson = jsonfromfile['soap:Body']['GetInventoryCalcAlarmResponse']['GetInventoryCalcAlarmResult']['CalcAlarmInventory'] #returns list
        #     listcount = len(listfromjson)
        listcount = 0
        try:
            listfromjson = jsonfromfile['soap:Body']['GetInventoryCalcAlarmResponse']['GetInventoryCalcAlarmResult']['CalcAlarmInventory'] #returns list
            for k in listfromjson:
                if k['iInventoryID']:
                    listcount += 1
        except KeyError:
            pass
            #log key error, ignore?
        return listcount

    def get_inventory_list(self):
        '''Get inventory list. Returns list of inventory IDs'''
        jsonfromfile = self.get_json_file(self.inventoryfile)

        returnlist = []
        #check for key error
        try:
            listfromjson = jsonfromfile['soap:Body']['GetInventoryResponse']['GetInventoryResult']['Inventory'] #returns list
            for k in listfromjson:
                if k['iInventoryID']:
                    returnlist.append(k['iInventoryID'])
        except KeyError:
            pass
            #log key error, ignore?
        return returnlist

    def get_tankinv_list(self):
        '''Get tank inventory list. 
        Returns list of tank IDs with inventory IDs'''
        #NOTE: Updated to use GetInventoryCalcAlarm LATEST instead of GetInventory or GetInventoryCalcAlarm
        tankjsonfromfile = self.get_json_file(self.tankjsonfile)
        #invjsonfromfile = self.get_json_file(self.inventoryfile)
        invjsonfromfile = self.get_json_file(self.invcalcalrmfilelatest)

        returnlist = []
        tanklistfromjson = tankjsonfromfile['soap:Body']['GetTankResponse']['GetTankResult']['Tank'] #returns list
        #invlistfromjson = invjsonfromfile['soap:Body']['GetInventoryResponse']['GetInventoryResult']['Inventory'] #returns list
        invlistfromjson = invjsonfromfile['soap:Body']['GetInventoryCalcAlarmResponse']['GetInventoryCalcAlarmResult']['CalcAlarmInventory'] #returns list
        for k in tanklistfromjson:
            try:
                #now iterate through each tank
                if k['iTankID']:
                    listelementtoappend = [] #need combo of k['iTankID'] AND k['iInventoryID']
                    for k2 in invlistfromjson:
                        try:
                            #check tank id against each item in inv to add all inv records for that tank id
                            if str(k['iTankID']) == str(k2['iTankID']) and k2['iInventoryID']:
                                listelementtoappend.append(k2['iInventoryID'])
                        except KeyError:
                            pass
                            #log key error?
                    tankid_dict = {k['iTankID'] : listelementtoappend} #create dict with key=tankID and value=list of invIDs
                    returnlist.append(tankid_dict)
            except KeyError:
                pass
                #log key error?
        return returnlist

    def get_latestinvid_bytank(self, tankidstr):
        '''Get the latest inventory id by tank id. 
        Return inventory id string'''
        returnlatestinvstr = ''
        bothlist = self.get_tankinv_list()
        for item in bothlist:
            try:
                if item[tankidstr]:
                    highestvalue = 0
                    valuelist = item[tankidstr]
                    for v in valuelist:
                        if int(v) > highestvalue:
                            highestvalue = int(v)
                    returnlatestinvstr = str(highestvalue)
            except KeyError:
                pass
        return returnlatestinvstr

    def get_grossvol_byinvid(self, invidstr):
        '''Get the gross volume from GetInventoryReponse based on inventory id. 
        Return gross inventory value as string'''
        #NOTE: Updated to use GetInventoryCalcAlarm LATEST instead of GetInventory or GetInventoryCalcAlarm
        # jsonfromfile = self.get_json_file(self.inventoryfile)
        jsonfromfile = self.get_json_file(self.invcalcalrmfilelatest)

        #check for key error
        try:
            # listfromjson = jsonfromfile['soap:Body']['GetInventoryResponse']['GetInventoryResult']['Inventory'] #returns list
            listfromjson = jsonfromfile['soap:Body']['GetInventoryCalcAlarmResponse']['GetInventoryCalcAlarmResult']['CalcAlarmInventory'] #returns list
            for k in listfromjson:
                if str(k['iInventoryID']) == invidstr:
                    return str(k['dGrossVolume'])
        except KeyError:
            pass
            #log key error, ignore?
        return ''

    def get_tankname_bytankid(self, tankidstr, tankdict):
        '''Get the tank name attribute from the parsed tank dictionary & tank id as a string. 
        Return tank name'''

        #check for key error
        try:
            dictfromjson = tankdict['soap:Body']['GetTankGeneralLatLonPlusResponse']['GetTankGeneralLatLonPlusResult'] #returns dict
            if str(dictfromjson['iTankID']) == tankidstr:
                return str(dictfromjson['sTankName'])
        except KeyError:
            pass
            #log key error, ignore?
        return ''

    def get_tankname_bytankid_file(self, tankidstr):
        '''Get the tank name attribute from the tank id as a string. 
        Return tank name'''
        uniquefilestr = self.tankgenlatlonplus.format(tankidstr)
        jsonfromfile = self.get_json_file(uniquefilestr)

        return self.get_tankname_bytankid(tankidstr, jsonfromfile)

    def get_tankalrm_byinvid(self, invalrmidstr):
        '''Get the alarm status for tank by the inventory id as a string. 
        Return the alarm status as string.'''
        #NOTE: Updated to use GetInventoryCalcAlarm LATEST instead of GetInventory or GetInventoryCalcAlarm
        jsonfromfile = self.get_json_file(self.invcalcalrmfilelatest)
        try:
            alrmlistfromjson = jsonfromfile['soap:Body']['GetInventoryCalcAlarmResponse']['GetInventoryCalcAlarmResult']['CalcAlarmInventory'] #returns list
            for k in alrmlistfromjson:
                if str(k['iInventoryID']) == invalrmidstr:
                    return str(k['iCalcAlarmBits'])
        except KeyError:
            print('key error')
        return ''
