import gateway
import soapreqs
import requests
import time, datetime

def logit(strtoadd):
    '''Add str text to log file'''
    try:
        with open('logs/runlog.txt', 'a') as text_file:
            text_file.write(strtoadd)
        return True
    except FileNotFoundError:
        return False

def cleanup_uniqueinvfiles():
    '''Delete all unique historical GetInventoryCalcAlarmResponse files from project data folder
    Returns True/False completion'''
    #TODO Implement and test this.
    return False

def build_latest_inv_file():
    '''NEW TEST TO GET LATEST INV RECORDS - THIS PROCESS GIVES YOU LATEST UNIQUE INVCALCALARM
    NOTE: THIS METHOD OF GETTING LATEST INVENTORY ONLY WORKS IF YOU HAVE LESS THAN 100 TANKS!'''
    #THIS FUNCTION SEEMS TO WORK WELL NOW
    try:
        logtxt = ''
        # g = gateway.Gateway()
        firstresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_soap()))
        g.save_resp_json(firstresponse)

        # Everything depends on count of this first item
        # p = gateway.Process()
        thecount = p.count_inventorycalcalrm()
        transactidstr = p.get_inventorycalcalrm_transactID()
        print('Inventory count: ' + str(thecount))
        if thecount <= 0:
            #No new inv, Use latest unique - BASICALLY THIS MEANS NEED TO COMPARE EMPTY GetInventoryCalcAlarmResponse.json
            #FILE TO THE LATEST GetInventoryCalcAlarmResponse_latest.json INVENTORY THAT SOULD ALREADY EXIST
            print('Zero new inventory records, use the existing latest')
        elif thecount >= 100:
            #ITERATE TO GET THE LATEST INVENTORY GetInventoryCalcAlarmResponse_latest.json; ALSO DEL EMPTY LATEST IF PRESENT AT END!
            print('100+ unprocessed inventory records, need to iterate to latest')
            print('TransactionID: ' + transactidstr)
            #get and save unique json reponse
            uniquedictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(transactidstr)))
            g.save_resp_unique_json(uniquedictresponse, transactidstr)
            #get the new inv alarm count from the uniquedictresponse
            invalrmcount = p.count_inventorycalcalrm_unique(transactidstr)
            print(' NEW Inv Count: ' + str(invalrmcount))
            #set transactid and count to first one above
            #nextinvalrmcount = invalrmcount
            nextinvalrmcount = thecount
            nexttransactidstr = transactidstr
            newuniquedictresponse = [] #used to store the next dict response
            nexttolastdictreponse = [] #used to store the previous next dict reponse, accounts for empty json file
            # while more to get, set new transactid to that from latest unique json
            while True:
                #save next to last id string in case last item has zero records
                nexttolastidstr = nexttransactidstr
                nexttolastdictreponse = newuniquedictresponse #save this for last iteration, in case of empty last json file
                #break while loop if count less than 100
                if nextinvalrmcount < 100:
                    break
                print('fetching next...')
                newtransactidstr = p.get_inventorycalcalrm_unique_transactID(nexttransactidstr)
                print('NEW TransactionID: ' + newtransactidstr)
                #get the next unique json from gateway request
                newuniquedictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(newtransactidstr)))
                g.save_resp_unique_json(newuniquedictresponse, newtransactidstr)
                #get the new inv alrm count from the newtransactidstr
                newinvalrmcount = p.count_inventorycalcalrm_unique(newtransactidstr)
                print(' NEW Inv Count: ' + str(newinvalrmcount))
                #update nexttransactid and nextinvalrmcount
                nexttransactidstr = p.get_inventorycalcalrm_unique_transactID(nexttransactidstr)
                nextinvalrmcount = p.count_inventorycalcalrm_unique(nexttransactidstr)
                time.sleep(1)
            #now, check if latest unique json has no records, if so delete it
            if len(nexttolastidstr) > 0 and newinvalrmcount < 1:
                newuniquedictresponse = nexttolastdictreponse #reset the latest to the one before that, because last one is empty
                deletresponsestr = 'data/GetInventoryCalcAlarmResponse{0}.json'
                g.delete_resp_unique_json(deletresponsestr.format(nexttransactidstr)) #delete the extra empty unique json file
            #finally, save the latest non-empty unique inv json file to the latest
            g.save_resp_unique_json(newuniquedictresponse, '_latest') #now this thould be the last and latest unique response
        else:
            #save as latest inv json file
            g.save_resp_unique_json(firstresponse, str(transactidstr)) #TODO is this needed?
            time.sleep(1)
            g.save_resp_unique_json(firstresponse, '_latest')
            print('New inventory saved to latest')
            #also get and save unique json reponse for the next transactid - IMPORTANT: THIS WILL GIVE AN EMPTY NEXT REPONSE
            lastdictresponse = g.parse_response(g.gateway_request(soapreqs.get_invalrm_transactid_soap(transactidstr)))
            g.save_resp_json(lastdictresponse)
    except:
        logtxt = 'error'
    return logtxt


# SETUP RUN TEST TO CHECK FOR CHANGES VIA GATEWAY
# TODO: Switch print stmts to log statements
print('\nWELCOME TO THE GATEWAY DEMO APP\n--------------------------------')
g = gateway.Gateway()
p = gateway.Process()
while True:
    print(str(datetime.datetime.now()) + ' - wake up...')
    #step1 - request all tanks and write to master tanks file
    print('step1 - requesting tanks...')
    g.save_resp_json(g.parse_response(g.gateway_request(soapreqs.get_tank_soap())))
    time.sleep(1)
    #step2 - build tank list from file created in step 1 and get latest inventory and alarm info
    tanklist = p.get_tank_list() #gives list of tank ids
    print('TankIDs: ' + str(tanklist))
    print('step2 - retrieving & writing latest inventory data to file...')
    for item in tanklist: #for each unique tank, create a unique file for each tank
        g.save_resp_unique_json(g.parse_response(g.gateway_request(soapreqs.get_tankgenlatlon_soap(item))), item)
        time.sleep(1)
    build_latest_inv_file() #get latest inv and save file
    #next, for each tank in tanklist display the latest inventory and alarms - now uses GetInventoryCalcAlarm
    clatankidlist = []
    for item in tanklist:
        latestinvidstr = p.get_latestinvid_bytank(str(item)) #get the latest inventory id for the tank
        alarmstatus = p.get_tankalrm_byinvid(latestinvidstr)
        #print('latest inv id: ' + latestinvidstr)
        if alarmstatus != '0':
            print('Tank ' + p.get_tankname_bytankid_file(str(item)) + ' currently has gross vol of '
                + p.get_grossvol_byinvid(latestinvidstr) + ' gals with alarm status ' + alarmstatus)
            if alarmstatus == '4':
                #tank is in critical low alarm (4) status, alarmstatus 8 indicates LA
                clatankidlist.append(str(item))
        else:
            print('Tank ' + p.get_tankname_bytankid_file(str(item)) + ' currently has gross vol of '
                + p.get_grossvol_byinvid(latestinvidstr) + ' gals')
    # #step 3 - now for tanks in CLA state, make call to proxy sim API to fill tank
    # print('step3 - make API call to fill tanks in CLA...')
    # #print('Tanks in CLA: ' + str(clatankidlist))
    # #TODO: see code/notes in test.py for the API call section, must be tested on machine running API for now
    # for clatank in clatankidlist:
    #     url = 'http://localhost:5000/api/tank/fill/?id={0}&amt={1}'
    #     apiidstr = p.get_tankname_bytankid_file(str(clatank))
    #     intforapi = int(apiidstr[3:]) #convert string name like sim01 to int like 01
    #     r = requests.get(url.format(str(intforapi), '6000')) #make call to Proxy Tank Sim API to fill tank
    #     print(r.text)
    #     time.sleep(1)
    print('zzzzz...')
    time.sleep(180)    #sleep for 3mins, increase this later
