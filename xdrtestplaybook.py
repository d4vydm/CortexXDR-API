import sys
import os
import time

from xdr_api_wrapper import *




##################################################
## Helper functions
def writeJsonToFile(filename, jsondata):
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(jsondata, outfile, indent=4)

    return 1

def printSep():
    i=os.get_terminal_size().columns
    while i > 0: i-=1; print("-", end = '')







##################################################
## Call functions
def executeCall(xdrclient, command, params, data):
    print(f'Command {command} called')
    try:
        if command == 'xdr_get_endpoint':
            # Get the Agents, and their data
            resp = get_endpoint(xdrclient, data)
            return resp

        elif command == 'xdr_get_incidents':
            # Get the Agents, and their data
            resp = get_incidents(xdrclient, data)
            return resp
        
        elif command == 'xdr_get_alerts':
            # Get the Agents, and their data
            resp = get_alerts(xdrclient, data)
            return resp

        else:
            errmsg = f'Command {command} not found'
            print(errmsg)
            raise ApiError(errmsg)

    # Log exceptions
    except Exception as e:
        error_message = f'Failed to execute {command} command. Error: '
        print(error_message + str(e.args[0]))

    return 0



##################################################
## Cortex XDR test playbook
def XDRplaybook(config_file):
    # Create Cortex XDR api client
    client = XDRClient(config_file)

    # #Get Incident
    # print('\n\n### Get Incidents')
    # command = 'xdr_get_incidents'
    # data = '{"request_data":{}}'
    # resp = executeCall(client, command, None, data)
    # if resp != 0:
    #     print("\nResult:\n" + resp)
    #     printSep()


    # #Get Incident Extra Data (incident_id: 3)
    # print('\n\n### Get Incidents')
    # command = 'xdr_get_incidents'
    # data = '{\
    #     "request_data": {\
    #         "incident_id": "3",\
    #         "alerts_limit": 20\
    #     }\
    # }'
    # resp = executeCall(client, command, None, data)
    # if resp != 0:
    #     print("\nResult:\n" + resp)
    #     printSep()

    #Get Endpoints
    print('\n\n### Get Endpoints')
    command = 'xdr_get_endpoint'
    endpointgroup = "Cortex-Silverfort"
    
    data = """
    {{
        "request_data": {{
            "filters": [
                {{
                    "field": "group_name",
                    "operator": "in",
                    "value": [
                        "{endpointgroupname}"
                    ]
                }}
            ]
        }}
    }}""".format(endpointgroupname=endpointgroup)
    resp = executeCall(client, command, None, data)
    if resp != 0:
        print("\nResult:\n" + resp)
        printSep()


    # #Get Alerts
    # print('\n\n### Get Alerts')
    # command = 'xdr_get_alerts'
    # data = """
    #     {{
    #         "request_data": {{
    #             "filters": [
    #                 {{
    #                     "field": "creation_time",
    #                     "operator": "gte",
    #                     "value": {currenttime}
    #                 }}
    #             ],
    #             "search_from": 0,
    #             "search_to": 100,
    #             "sort": {{
    #                 "field": "creation_time",
    #                 "keyword": "desc"
    #             }}
    #         }}
    #     }}
    #     """.format(currenttime='1616501863003')

    # resp = executeCall(client, command, None, data)
    # if resp != 0:
    #     print("\nResult:\n" + resp)
    #     printSep()






if __name__ in ('__main__'):
    if len(sys.argv) < 2:
        print('Provide the path to the Cortex XDR API config file as argument')
        sys.exit()

    config_file = sys.argv[1]

    if not os.path.isfile(config_file):
        print('The specified file does not exist')
        sys.exit()

    # Read config file
    with open(config_file, "r") as read_file:
        config = json.load(read_file)

    # Run a test on the sentinal one api
    XDRplaybook(config)
