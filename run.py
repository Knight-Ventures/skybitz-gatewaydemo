#!flask/bin/python
import gateway
import soapreqs
import time, datetime

# SETUP RUN TEST TO CHECK FOR CHANGES VIA GATEWAY
print('\nWELCOME TO THE GATEWAY DEMO APP\n--------------------------------')
g = gateway.Gateway()
p = gateway.Process()
while True:
    print(str(datetime.datetime.now()) + ' - wake up...')
    #step1 - req all tanks and write to master tanks file
    g.save_resp_json(g.parse_response(g.gateway_request(soapreqs.get_tank_soap())))
    time.sleep(1)
    print('retrieved tanks...')
    #step2 - build tank list from file created in step 1
    tanklist = p.get_tank_list() #gives list of tank ids
    print('TankIDs: ' + str(tanklist))
    for item in tanklist: #for each unique tank, create a unique file for each tank
        g.save_resp_unique_json(g.parse_response(g.gateway_request(soapreqs.get_tankgenlatlon_soap(item))), item)
        time.sleep(1)
    #step3 - get latest inv and save file
    print('writing parsed inventory data to file...')
    g.save_resp_json(g.parse_response(g.gateway_request(soapreqs.get_inv_soap())))
    print('writing parsed alarm data to file...')
    g.save_resp_json(g.parse_response(g.gateway_request(soapreqs.get_invalrm_soap())))
    #delay
    print('zzzzz')
    time.sleep(180)    #sleep for 3mins, increase this later
