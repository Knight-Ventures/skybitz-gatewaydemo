import gateway

#Used for testing only
import pprint
import json

g = gateway.Gateway()

#soapResponse = g.gatewayRequest(g.soapGetOrganization())
#soapResponse = g.gatewayRequest(g.soapGetLocation())
soapResponse = g.gatewayRequest(g.soapGetTank())

dictPayload = g.parseXML2dict(soapResponse)

result = g.parseXML2json(dictPayload)

#TEST SECTION ONLY
#print(soapResponse.content)
pprint.pprint(dictPayload)
#print('+++++++++++++++++++++++++')
#print(json.dumps(json.loads(result), sort_keys=True, indent=4))

f = open('temp.json', 'w')
f.write(json.dumps(json.loads(result), sort_keys=True, indent=4))