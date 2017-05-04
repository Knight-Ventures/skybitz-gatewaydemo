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


# # NEW TEST TO GET LATEST INV RECORDS - THIS PROCESS GIVES YOU LATEST UNIQUE INVCALCALARM
# #NOTE: THIS METHOD OF GETTING LATEST INVENTORY ONLY WORKS IF YOU HAVE LESS THAN 100 TANKS!
# #TODO: Place thi ALL into a function that whose job is to basically create the latest inventory json file.
# g = gateway.Gateway()
# firstresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_soap()))
# g.save_resp_json(firstresponse)

# # Everything depends on count of this first item
# p = gateway.Process()
# thecount = p.count_inventorycalcalrm()
# transactidstr = p.get_inventorycalcalrm_transactID()
# print('TransactID: ' + transactidstr)
# print('Inventory count: ' + str(thecount))
# #IF COUNT <= 0 --> NO NEW INV RECORDS
#         #MUST USE LATEST UNIQUE JSON FILE FOR INV RECORDS
# #ELSE IF COUNT >= 100 --> NEED TO ITERATE THRU TO GET LATEST
#         #MUST MAKE SURE YOU SAVE EACH UNIQUE JSON! ONCE YOU CALL THE WEB SERVICE WITH TRANSACTID, YOU CANNOT GET IT AGAIN!
# #ELSE YOU HAVE THE LATEST INV IN GetInventoryCalcAlarmResponse.json, SAVE TO LATEST
# if thecount <= 0:
#     #No new inv, Use latest unique - BASICALLY THIS MEANS NEED TO COMPARE EMPTY GetInventoryCalcAlarmResponse.json
#     #FILE TO THE LATEST GetInventoryCalcAlarmResponse_latest.json INVENTORY THAT SOULD ALREADY EXIST
#     print('Zero new inventory records, use the existing latest')
# elif thecount >= 100:
#     #ITERATE TO GET THE LATEST INVENTORY GetInventoryCalcAlarmResponse_latest.json; ALSO DEL EMPTY LATEST IF PRESENT AT END!
#     print('more than 100, need to iterate to latest')
#     #transactidstr = p.get_inventorycalcalrm_transactID()
#     #invalrmcount = p.count_inventorycalcalrm()
#     print('TransactionID: ' + transactidstr)
#     #get and save unique json reponse
#     uniquedictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(transactidstr)))
#     g.save_resp_unique_json(uniquedictresponse, transactidstr)
#     #get the new inv alarm count from the uniquedictresponse
#     invalrmcount = p.count_inventorycalcalrm_unique(transactidstr)
#     print(' NEW Inv Count: ' + str(invalrmcount))
#     #set transactid and count to first one above
#     #nextinvalrmcount = invalrmcount
#     nextinvalrmcount = thecount
#     nexttransactidstr = transactidstr
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
#         time.sleep(2)
#     #now, check if latest unique json has no records, if so delete it
#     if len(nexttolastidstr) > 0 and newinvalrmcount < 1:
#         deletresponsestr = 'data/GetInventoryCalcAlarmResponse{0}.json'
#         g.delete_resp_unique_json(deletresponsestr.format(nexttransactidstr))
#     #finally, save the latest non-empty unique inv json file to the latest
#     g.save_resp_unique_json(newuniquedictresponse, '_latest')
# else:
#     print('Less than 100')
#     #save as latest inv json file
#     g.save_resp_unique_json(firstresponse, '_latest')
#     # #also get and save unique json reponse for the next transactid - IMPORTANT: THIS WILL GIVE AN EMPTY NEXT REPONSE
#     # uniquedictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(transactidstr)))
#     # g.save_resp_unique_json(firstresponse, transactidstr)



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
# #TODO: Add function in Process to perform an alarm bits lookup to decode the actual alarm state


# #RUN.PY TEST
# # SETUP RUN TEST TO CHECK FOR CHANGES VIA GATEWAY
# # TODO: Switch print stmts to log statements
# print('\nWELCOME TO THE GATEWAY DEMO APP\n--------------------------------')
# g = gateway.Gateway()
# p = gateway.Process()
# while True:
#     print(str(datetime.datetime.now()) + ' - wake up...')
#     #step1 - request all tanks and write to master tanks file
#     g.save_resp_json(g.parse_response(g.gateway_request(soapreqs.get_tank_soap())))
#     time.sleep(1)
#     print('retrieved tanks...')
#     #step2 - build tank list from file created in step 1
#     tanklist = p.get_tank_list() #gives list of tank ids
#     print('TankIDs: ' + str(tanklist))
#     for item in tanklist: #for each unique tank, create a unique file for each tank
#         g.save_resp_unique_json(g.parse_response(g.gateway_request(soapreqs.get_tankgenlatlon_soap(item))), item)
#         time.sleep(1)
#     #step3 - get latest inv and save file
#     print('writing parsed inventory data to file...')
#     g.save_resp_json(g.parse_response(g.gateway_request(soapreqs.get_inv_soap())))
#     print('writing parsed alarm data to file...')
#     g.save_resp_json(g.parse_response(g.gateway_request(soapreqs.get_invalrm_soap())))
#     #delay
#     print('zzzzz')
#     time.sleep(180)    #sleep for 3mins, increase this later



# def build_latest_inv_file():
#     '''NEW TEST TO GET LATEST INV RECORDS - THIS PROCESS GIVES YOU LATEST UNIQUE INVCALCALARM
#     NOTE: THIS METHOD OF GETTING LATEST INVENTORY ONLY WORKS IF YOU HAVE LESS THAN 100 TANKS!'''
#     try:
#         logtxt = ''
#         g = gateway.Gateway()
#         firstresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_soap()))
#         g.save_resp_json(firstresponse)

#         # Everything depends on count of this first item
#         p = gateway.Process()
#         thecount = p.count_inventorycalcalrm()
#         transactidstr = p.get_inventorycalcalrm_transactID()
#         print('TransactID: ' + transactidstr)
#         print('Inventory count: ' + str(thecount))
#         #IF COUNT <= 0 --> NO NEW INV RECORDS
#                 #MUST USE LATEST UNIQUE JSON FILE FOR INV RECORDS
#         #ELSE IF COUNT >= 100 --> NEED TO ITERATE THRU TO GET LATEST
#                 #MUST MAKE SURE YOU SAVE EACH UNIQUE JSON! ONCE YOU CALL THE WEB SERVICE WITH TRANSACTID, YOU CANNOT GET IT AGAIN!
#         #ELSE YOU HAVE THE LATEST INV IN GetInventoryCalcAlarmResponse.json, SAVE TO LATEST
#         if thecount <= 0:
#             #No new inv, Use latest unique - BASICALLY THIS MEANS NEED TO COMPARE EMPTY GetInventoryCalcAlarmResponse.json
#             #FILE TO THE LATEST GetInventoryCalcAlarmResponse_latest.json INVENTORY THAT SOULD ALREADY EXIST
#             print('Zero new inventory records, use the existing latest')
#         elif thecount >= 100:
#             #ITERATE TO GET THE LATEST INVENTORY GetInventoryCalcAlarmResponse_latest.json; ALSO DEL EMPTY LATEST IF PRESENT AT END!
#             print('more than 100, need to iterate to latest')
#             #transactidstr = p.get_inventorycalcalrm_transactID()
#             #invalrmcount = p.count_inventorycalcalrm()
#             print('TransactionID: ' + transactidstr)
#             #get and save unique json reponse
#             uniquedictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(transactidstr)))
#             g.save_resp_unique_json(uniquedictresponse, transactidstr)
#             #get the new inv alarm count from the uniquedictresponse
#             invalrmcount = p.count_inventorycalcalrm_unique(transactidstr)
#             print(' NEW Inv Count: ' + str(invalrmcount))
#             #set transactid and count to first one above
#             #nextinvalrmcount = invalrmcount
#             nextinvalrmcount = thecount
#             nexttransactidstr = transactidstr
#             # while more to get, set new transactid to that from latest unique json
#             while True:
#                 #save next to last id string in case last item has zero records
#                 nexttolastidstr = nexttransactidstr
#                 #break while loop if count less than 100
#                 if nextinvalrmcount < 100:
#                     break
#                 print('fetching next...')
#                 newtransactidstr = p.get_inventorycalcalrm_unique_transactID(nexttransactidstr)
#                 print('NEW TransactionID: ' + newtransactidstr)
#                 #get the next unique json from gateway request
#                 newuniquedictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(newtransactidstr)))
#                 g.save_resp_unique_json(newuniquedictresponse, newtransactidstr)
#                 #get the new inv alrm count from the newtransactidstr
#                 newinvalrmcount = p.count_inventorycalcalrm_unique(newtransactidstr)
#                 print(' NEW Inv Count: ' + str(newinvalrmcount))
#                 #update nexttransactid and nextinvalrmcount
#                 nexttransactidstr = p.get_inventorycalcalrm_unique_transactID(nexttransactidstr)
#                 nextinvalrmcount = p.count_inventorycalcalrm_unique(nexttransactidstr)
#                 time.sleep(2)
#             #now, check if latest unique json has no records, if so delete it
#             if len(nexttolastidstr) > 0 and newinvalrmcount < 1:
#                 deletresponsestr = 'data/GetInventoryCalcAlarmResponse{0}.json'
#                 g.delete_resp_unique_json(deletresponsestr.format(nexttransactidstr))
#             #finally, save the latest non-empty unique inv json file to the latest
#             g.save_resp_unique_json(newuniquedictresponse, '_latest')
#         else:
#             print('Less than 100')
#             #save as latest inv json file
#             g.save_resp_unique_json(firstresponse, '_latest')
#             # #also get and save unique json reponse for the next transactid - IMPORTANT: THIS WILL GIVE AN EMPTY NEXT REPONSE
#             # uniquedictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(transactidstr)))
#             # g.save_resp_unique_json(firstresponse, transactidstr)
#     except:
#         logtxt = 'error'
#     return logtxt



# # TEST 9 - modified test #8 for using latest inv above based on count
# g = gateway.Gateway()
# p = gateway.Process()
# #step1 - req all tanks and write to master tanks file
# g.save_resp_json(g.parse_response(g.gateway_request(soapreqs.get_tank_soap())))
# time.sleep(2)
# #step2 - build tank list from file created in step 1
# tanklist = p.get_tank_list() #gives list of tank ids - THIS IS AN IMPORTANT STEP FOR SEVERAL ITEMS BELOW!!!!!!!
# #print(tanklist)
# for item in tanklist: #for each unique tank, create a unique json file for each tank
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





