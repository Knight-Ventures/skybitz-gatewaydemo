import gateway
import soapreqs
import time
from datetime import datetime

#Imports currently used for testing only
# import pprint
# import json

# --------------------------------------------------------- #
''' EARLY TEST SCENARIOS '''
# --------------------------------------------------------- #
# invalrmlist = d['soap:Body']['GetInventoryCalcAlarmResponse']['GetInventoryCalcAlarmResult']['CalcAlarmInventory']
# inventorytime = ''
# for item in invalrmlist:
#     if item['sUTCInventoryTime']:
#         #datetime_object = datetime.strptime(str(item['sUTCInventoryTime']), '%m %d %Y %I:%M:%S %p')
#         print(str(item['sUTCInventoryTime']))
#     # if item['iCalcAlarmBits'] != str(0):
#     #     print('Tank ' + item['iTankID'] + ' has alarm status ' + item['iCalcAlarmBits'])

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


# --------------------------------------------------------- #
''' REAL GATEWAY TEST SECTION '''
# --------------------------------------------------------- #

# GATEWAY SOAP GEN AND REQUEST TESTS
# g = gateway.Gateway()
# Make the Request to Gateway
# soapResponse = g.gateway_request(soapreqs.get_org_soap())
# soapResponse = g.gateway_request(soapreqs.get_loc_soap())
# soapResponse = g.gateway_request(soapreqs.get_tank_soap())
# soapResponse = g.gateway_request(soapreqs.get_inv_soap())
# soapResponse = g.gateway_request(soapreqs.get_invalrm_soap())
# tankgenlatlonstr = '10203647'
# soapResponse = g.gateway_request(soapreqs.get_tankgenlatlon_soap(tankgenlatlonstr))
# # Parse response
# dresp = g.parse_response(soapResponse)
# print(dresp)

# INV ALARM CALC TRANSACTIONID TESTS
# # Step1 - make request using simple inventory soap (ie. zero as ACK code), parse response and save json file
# g = gateway.Gateway()
# dictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_soap())) #soapreqs.get_invalrm_transactid_soap('0') works the same
# # Step2 - Process the json file to get the TransactionID and Inv Calc Alarm count
# p = gateway.Process()
# transactidstr = p.get_inventorycalcalrm_transactID()
# invalrmcount = p.count_inventorycalcalrm()
# print('TransactionID: ' + transactidstr + ' Inv Count: ' + str(invalrmcount))
# time.sleep(2) #wait 2 secs
# #Step2.5 - make a second gateway req using the TransactionID to create unique json - first test
# testinvtransactid = '47174434'
# #g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(testinvtransactid)))
# newinvalrmcount = p.count_inventorycalcalrm_unique(testinvtransactid)
# print('new count: ' + str(newinvalrmcount))
# #Step3 - make a second gateway request using the TransactionID to create unique json file
# uniquedictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(transactidstr)))
# g.save_resp_unique_json(uniquedictresponse, transactidstr)
# #Step4 - Now parse the unique json file to get the new transaction id and count
# newtransactidstr = p.get_inventorycalcalrm_unique_transactID(transactidstr)
# newinvalrmcount = p.count_inventorycalcalrm_unique(transactidstr)
# print('NEW TransactionID: ' + newtransactidstr + ' NEW Inv Count: ' + str(newinvalrmcount))
# #Step 5- Repeat as neccessary until count < 100 to get the latest inventory
# nexttransactidstr = transactidstr
# newinvalrmcount = invalrmcount
# while newinvalrmcount == 100:
#     time.sleep(3)
#     #replaces step3
#     uniquedictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(nexttransactidstr)))
#     g.save_resp_unique_json(uniquedictresponse, nexttransactidstr)
#     print('Created unique json for TransactionID ' + nexttransactidstr)
#     #replaces step4
#     newinvalrmcount = p.count_inventorycalcalrm_unique(nexttransactidstr) #updates newinvalrmcount
#     newtransactidstr = p.get_inventorycalcalrm_unique_transactID(nexttransactidstr) #temp var
#     print('NEW TransactionID: ' + nexttransactidstr + ' NEW Inv Count: ' + str(newinvalrmcount))
#     nexttransactidstr = newtransactidstr #updates nexttransactidstr


# NEW TEST TO GET LATEST INV RECORDS - THIS PROCESS GIVES YOU LATEST UNIQUE INVCALCALARM
#NOTE: THIS METHOD ONLY WORKS IF YOU HAVE LESS THAN 100 TANKS!
g = gateway.Gateway()
g.save_resp_json(g.parse_response(g.gateway_request(soapreqs.get_invalrm_soap())))

# Everything depends on count of this first item
p = gateway.Process()
print(str(p.count_inventorycalcalrm()))
#IF COUNT <= 0 --> NO NEW INV RECORDS
        #MUST USE LATEST UNIQUE JSON FILE FOR INV RECORDS
#ELSE IF COUNT >= 100 --> NEED TO ITERATE THRU TO GET LATEST
        #MUST MAKE SURE YOU SAVE EACH UNIQUE JSON! ONCE YOU CALL THE WEB SERVICE WITH TRANSACTID, YOU CANNOT GET IT AGAIN!
#ELSE YOU HAVE THE LATEST INV IN GetInventoryCalcAlarmResponse.json, SAVE TO LATEST


# transactidstr = p.get_inventorycalcalrm_transactID()
# # invalrmcount = p.count_inventorycalcalrm()
# print('TransactionID: ' + transactidstr)
# #get and save unique json reponse
# uniquedictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(transactidstr)))
# g.save_resp_unique_json(uniquedictresponse, transactidstr)
# #get the new inv alarm count from the uniquedictresponse
# invalrmcount = p.count_inventorycalcalrm_unique(transactidstr)
# print(' NEW Inv Count: ' + str(invalrmcount))
# #determine inv count - if less than 100, nothing more to do
# nexttolastidstr = ''
# newuniquedictresponse = []
# if invalrmcount == 100:
#     print('more than 100, need to iterate to latest')
#     #set transactid and count to first one above
#     nexttransactidstr = transactidstr
#     nextinvalrmcount = invalrmcount
#     # while more to get, set new transactid to that from latest unique json
#     while True:
#         #save next to last id string in case last item has zero records
#         nexttolastidstr = nexttransactidstr
#         #break while loop if count less than 100
#         if nextinvalrmcount < 100:
#             break
#         print('fetching next...')
#         newtransactidstr = p.get_inventorycalcalrm_unique_transactID(nexttransactidstr)
#         print('NEW TransactionID: ' + newtransactidstr)
#         #get the next unique json from gateway request
#         newuniquedictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(newtransactidstr)))
#         g.save_resp_unique_json(newuniquedictresponse, newtransactidstr)
#         #get the new inv alrm count from the newtransactidstr
#         newinvalrmcount = p.count_inventorycalcalrm_unique(newtransactidstr)
#         print(' NEW Inv Count: ' + str(newinvalrmcount))
#         #update nexttransactid and nextinvalrmcount
#         nexttransactidstr = p.get_inventorycalcalrm_unique_transactID(nexttransactidstr)
#         nextinvalrmcount = p.count_inventorycalcalrm_unique(nexttransactidstr)
#         time.sleep(3)
#     #now, check if latest unique json has no records, if so delete it
#     if len(nexttolastidstr) > 0 and newinvalrmcount < 1:
#         deletresponsestr = 'data/GetInventoryCalcAlarmResponse{0}.json'
#         g.delete_resp_unique_json(deletresponsestr.format(nexttransactidstr))
#     #finally, rename the unique inv json file to be the generic starting point GetInventoryCalcAlarmResponselatest json file!
#     if len(str(newuniquedictresponse)) > 0:
#         g.save_resp_unique_json(newuniquedictresponse, 'latest')
# else:
#     print('less than 100, have latest')
#     g.save_resp_unique_json(uniquedictresponse, 'latest')










# PROCESSING TEST SECTION ONLY
# p = gateway.Process()
#test1
# tanklist = p.get_tank_list()
# for item in tanklist:
#     print(item)
#test2
# invlist = p.get_inventory_list()
# for item in invlist:
#     print(item)
#test3
# bothlist = p.get_tankinv_list()
# for item in bothlist:
#     print(item)
#test4
# print(p.get_grossvol_byinvid('194699940'))
#test5
# latestinvstr = p.get_latestinvid_bytank('10203647') #works!
# print(latestinvstr)
#test6 - nice working test!
# tanklist = p.get_tank_list() #gives list of tank ids
# print(tanklist)
# for item in tanklist: #display latest inventory for each tank in list
#     latestinvidstr = p.get_latestinvid_bytank(str(item)) #get the latest inventory id for the tank
#     print('TankID: ' + str(item) + ' currently has gross vol ' + p.get_grossvol_byinvid(latestinvidstr) + ' gals')
#test7
#print(str(p.get_tankname_bytankid('10203647')))


# # TEST 8 - full test working thru step 4 - fully working
# g = gateway.Gateway()
# p = gateway.Process()
# #step1 - req all tanks and write to master tanks file
# g.save_resp_json(g.parse_response(g.gateway_request(soapreqs.get_tank_soap())))
# time.sleep(2)
# #step2 - build tank list from file created in step 1
# tanklist = p.get_tank_list() #gives list of tank ids - THIS IS AN IMPORTANT STEP FOR SEVERAL ITEMS BELOW!!!!!!!
# #print(tanklist)
# for item in tanklist: #for each unique tank, create a unique file for each tank
#     g.save_resp_unique_json(g.parse_response(g.gateway_request(soapreqs.get_tankgenlatlon_soap(item))), item)
#     time.sleep(1)
# #step3 - get latest inv and save file
# g.save_resp_json(g.parse_response(g.gateway_request(soapreqs.get_inv_soap())))
# #step4 - for each tank in tanklist get latest inventory and display
# #note: for this to work, you must have already done steps 1 and 3 above - need tank and inv
# for item in tanklist:
#     latestinvidstr = p.get_latestinvid_bytank(str(item)) #get the latest inventory id for the tank
#     print('Tank ' + p.get_tankname_bytankid_file(str(item)) + ' currently has gross vol of '
#           + str(int(float(p.get_grossvol_byinvid(latestinvidstr)))) + ' gals')
# #step5 - works now, similar to step 4
# g.save_resp_json(g.parse_response(g.gateway_request(soapreqs.get_invalrm_soap())))
# #step7 - parse and display the data
# for item in tanklist:
#     latestinvidstr = p.get_latestinvid_bytank(str(item)) #get the latest inventory id for the tank
#     alarmstatus = p.get_tankalrm_byinvid(latestinvidstr)
#     if alarmstatus != '0':
#         print('Tank ' + p.get_tankname_bytankid_file(str(item)) + ' currently has alarm status of '
#               + alarmstatus + ' calc alarm bits')
# #TODO: Perform an alarm bits lookup to decode the actual alarm state


# --------------------------------------------------------- #
''' RUN TEST SECTION - MAKE AUTO CALLS TO PROXY SIM API'''
# --------------------------------------------------------- #

# SIMPLE TESTS MAKING CALLS TO PROXY TANK SIM API
# Should eventually config to make these auto calls based on alarm status
# # test1
# url = 'http://localhost:5000/api/tanks'
# r = requests.get(url)
# print(r.text)

# # test2
# url = 'http://localhost:5000/api/tanks/{0}'
# r = requests.get(url.format('s03'))
# print(r.text)

# # test3
# url = 'http://localhost:5000/api/tank/fill/?id={0}&amt={1}'
# r = requests.get(url.format('01', '50'))
# print(r.text)
