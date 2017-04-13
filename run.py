import gateway
import soapreqs

#Used for testing only
import pprint
import json

#g = gateway.Gateway()
#soapResponse = g.gatewayRequest(soapreqs.getOrgSoap())
#soapResponse = g.gatewayRequest(soapreqs.getLocSoap())
#soapResponse = g.gatewayRequest(soapreqs.getTankSoap())
#soapResponse = g.gatewayRequest(soapreqs.getInvSoap())
#d = g.parseResponse(soapResponse)

#TEST SECTION ONLY
p = gateway.Process()
tanklist = p.getTankList()
for item in tanklist:
    print(item)

#pprint.pprint(soapResponse + '\n')
#g.saveRespJSON(d)

# f = open('temp.json', 'w')
# f.write(json.dumps(resp, sort_keys=True, indent=4))

# for k in d['soap:Body']:
#     print(k)
#     break

# d = {'ONE':{'TWO':{'THREE':'some txt value'}}}
# pprint.pprint(d)
# print(d['ONE'])
# print(d['ONE']['TWO'])

# print(d['soap:Body']['GetTankResponse']['@xmlns'])
# print(d['soap:Body']['GetTankResponse']['iErrorCode'])
# tanklist = d['soap:Body']['GetTankResponse']['GetTankResult']['Tank']
# for item in tanklist:
#     print(item) #need to fix

# #Org example reading the list in Organization value
# print(d['soap:Body']['GetOrganizationResponse']['@xmlns'])
# print(d['soap:Body']['GetOrganizationResponse']['iErrorCode'])
# list = d['soap:Body']['GetOrganizationResponse']['GetOrganizationResult']['Organization'] #returns list
# for k in list:
#     #print(type(k))
#     #print(k)
#     for k, v in k.items():
#         if k == 'iOrganizationID':
            # print(k, v)
            # #print(v)

# #Loc example reading the list in Location value
# print('Return code: ' + str(d['soap:Body']['GetLocationResponse']['iErrorCode']))
# print('Location List: ')
# list = d['soap:Body']['GetLocationResponse']['GetLocationResult']['Location'] #returns list
# for k in list:
#     try:
#         if k['iLocationID']:
#             print('ID: ' + str(k['iLocationID']) + '    Name: ' + str(k['sLocationName'])
#             + '    Address: ' + str(k['sAddress1']))
#     except KeyError:
#         pass

# #Tank example reading the list in Tank value
# print('Return code: ' + str(d['soap:Body']['GetTankResponse']['iErrorCode']))
# print('Tank List: ')
# list = d['soap:Body']['GetTankResponse']['GetTankResult']['Tank'] #returns list
# for k in list:
#     try:
#         if k['iTankID']:
#             print('ID: ' + str(k['iTankID']))
#     except KeyError:
#         pass
