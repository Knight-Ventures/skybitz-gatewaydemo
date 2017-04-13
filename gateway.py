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

    def parseDictionary(self, d):
        '''Convert dict output from parseResponse to JSON.
        Returns json formatted string'''
        # return json.dumps(d)
        return json.dumps(d, sort_keys=True, indent=4)

    def saveRespJSON(self, resp):
        '''Save the dictionary formatted response from parseResponse to local JSON file.'''
        try:
            file = ''  #create json filename from root key
            for k in resp['soap:Body']:
                file = str(k) + '.json'
                break
            
            f = open(file, 'w')
            f.write(json.dumps(resp, sort_keys=True, indent=4))
            return True
        except:
            return False

class Process():
    '''Process class for processing data in JSON obtained from Gateway'''

    def __init__(self):
        '''Create process for reading data from json'''
        self.tankjsonfile = 'GetTankResponse.json'
    
    def getTankList(self):
        try:
            f = open(self.tankjsonfile, 'r')
            jsonfromfile = json.loads(f.read())
            print(jsonfromfile)
        except FileNotFoundError:
            print('filenotfound')
            jsonfromfile = '{ }'
        
        #TODO: Fix this, the try catch is for key error, should be inside the for loop
        #OTHERWISE, this section works well.
        returnlist = []
        try:
            list = jsonfromfile['soap:Body']['GetTankResponse']['GetTankResult']['Tank'] #returns list
            #print('list')
            for k in list:
                if k['iTankID']:
                    returnlist.append(k['iTankID'])
        except:
            print('error')
            pass
        return returnlist
