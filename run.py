import gateway
import soapreqs

#Used for testing only
import pprint
import json

g = gateway.Gateway()

soapResponse = g.gatewayRequest(soapreqs.getOrgSoap())
#soapResponse = g.gatewayRequest(soapreqs.getLocSoap())
#soapResponse = g.gatewayRequest(soapreqs.getTankSoap())
d = g.parseResponse(soapResponse)

#TEST SECTION ONLY
#pprint.pprint(soapResponse + '\n')

f = open('temp.json', 'w')
f.write(json.dumps(d, sort_keys=True, indent=4))

# d = {'ONE':{'TWO':{'THREE':'some txt value'}}}
# pprint.pprint(d)
# print(d['ONE'])
# print(d['ONE']['TWO'])

# print(d['soap:Body']['GetTankResponse']['@xmlns'])
# print(d['soap:Body']['GetTankResponse']['iErrorCode'])
# tanklist = d['soap:Body']['GetTankResponse']['GetTankResult']['Tank']
# for item in tanklist:
#     print(item) #need to fix

#Org example reading the ordered list in Organization value
print(d['soap:Body']['GetOrganizationResponse']['@xmlns'])
print(d['soap:Body']['GetOrganizationResponse']['iErrorCode'])
tanklist = d['soap:Body']['GetOrganizationResponse']['GetOrganizationResult']['Organization'] #returns list
for k in tanklist:
    #print(type(k))
    #print(k)
    for k, v in k.items():
        if k == 'iOrganizationID':
            print(k, v)
        # print(k, v)
        # print('\n')
