import requests
import json



# Suppress SSL warning
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)




##################################################
## APIError
class ApiError(Exception):
    """An API Error Exception"""
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "ApiError: status={}".format(self.status)





##################################################
## Cortex XDR API CLIENT
class XDRClient:
    def __init__(self, configfile):
        self.base_url = configfile['uri']
        self.api = configfile['api']
        self.api_key_id = configfile['api_key_id']
        self.api_key = configfile['api_key']
        

    def get_general_http_request(self, function):
        #Create API call URI
        fulluri = self.base_url \
            + self.api \
            + function

        #Call API
        resp = requests.get(
            url=fulluri,
            verify=False,
            headers={
                "x-xdr-auth-id": self.api_key_id,
                "Authorization": self.api_key,
                "Content-Type": "application/json"
            }
        )

        if resp.status_code != 200:
            raise ApiError(f'CALL {function} '.format(resp.status_code))
        else:
            return resp

    def post_general_http_request(self, function, data):
        #Create API call URI
        fulluri = self.base_url \
            + self.api \
            + function

        #Call API
        resp = requests.post(
            url=fulluri, 
            data=data, 
            verify=False, 
            headers={
                "x-xdr-auth-id": self.api_key_id,
                "Authorization": self.api_key,
                "Content-Type": "application/json"
            }
        )

        if resp.status_code != 200:
            raise ApiError(f'CALL {function} '.format(resp.status_code) + json.dumps(resp.json()))
        else:
            return resp

    def get_params_http_request(self, function, params):
        """
        Takes the params in json string format, like:
        {
            "param1": "value1",
            "param2": "value2"
        }
        The json param gets parsed to a uri string format and appended to the uri request
        """

        #Create the params in uri string format
        params_str=""
        if (params != ""):
            params_str="?"
            params_dict=json.loads(params)
            for f,v in params_dict.items():
                params_str+=f+"="+v+"&"
            params_str=params_str[:-1]

        #Create API call URI
        fulluri = self.base_url \
            + self.api \
            + function \
            + params_str

        #Call API
        resp = requests.get(
            url=fulluri,
            verify=False,
            headers={
                "x-xdr-auth-id": self.api_key_id,
                "Authorization": self.api_key,
                "Content-Type": "application/json"
            }
        )

        if resp.status_code != 200:
            raise ApiError(f'CALL {function} '.format(resp.status_code) + json.dumps(resp.json()))
        else:
            return resp

    def get_incidents_http_request(self, data):
        """
        # Get a list of incidents paramsed by a list of incident IDs, modification time, or creation time.
        # data is a json formatted body containting the request_data
        # https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/incident-management/get-incidents.html
        """

        function = "incidents/get_incidents/"
        return self.post_general_http_request(function, data)

    def get_incident_extra_data_http_request(self, data):
        """
        # Get extra data fields of a specific incident including alerts and key artifacts.
        # The API includes a limit rate of 10 API requests per minute.
        # https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/incident-management/get-extra-incident-data.html
        """

        function = "incidents/get_incident_extra_data/"
        return self.post_general_http_request(function, data)

    def get_endpoint_http_request(self, data):
        """
        # Gets a list of filtered endpoints
        # https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/endpoint-management/get-endpoints.html
        """

        function = "endpoints/get_endpoint/"
        return self.post_general_http_request(function, data)

    def get_alerts_http_request(self, data):
        """
        # Get a list of alerts with multiple events.
        # https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/incident-management/get-alerts.html
        """

        function = "alerts/get_alerts_multi_events/"
        return self.post_general_http_request(function, data)

    def isolate_endpoint_http_request(self, data):
        """
        # Isolate one or more endpoints in a single request. Request is limited to 1000 endpoints.
        # https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/response-actions/isolate-endpoints.html
        """

        function = "endpoints/isolate/"
        return self.post_general_http_request(function, data)


def get_incidents(xdrclient, data):
    """
    # Get a list of incidents paramsed by a list of incident IDs, modification time, or creation time.
    """

    resp = xdrclient.get_incidents_http_request(data)

    name = 'Cortex XDR Get Incidents'
    output = json.dumps({"APICall": name, "Response": resp.json()}, indent=4)

    return output

def get_incident_extra_data(xdrclient, data):
    """
    # Get extra data fields of a specific incident including alerts and key artifacts.
    """

    resp = xdrclient.get_incident_extra_data(data)

    name = 'Cortex XDR Get Incident Extra Data'
    output = json.dumps({"APICall": name, "Response": resp.json()}, indent=4)

    return output

def get_endpoint(xdrclient, data):
    """
    # Gets a list of filtered endpoints
    """

    resp = xdrclient.get_endpoint_http_request(data)

    name = 'Cortex XDR Get Endpoint'
    output = json.dumps({"APICall": name, "Response": resp.json()}, indent=4)

    return output

def get_alerts(xdrclient, data):
    """
    # Get a list of alerts with multiple events.
    """

    resp = xdrclient.get_alerts_http_request(data)

    name = 'Cortex XDR Get Alerts'
    output = json.dumps({"APICall": name, "Response": resp.json()}, indent=4)

    return output

def isolate_endpoint(xdrclient, data):
    """
    # Isolate one or more endpoints in a single request.
    """

    resp = xdrclient.isolate_endpoint_http_request(data)

    name = 'Cortex XDR Isolate Endpoints'
    output = json.dumps({"APICall": name, "Response": resp.json()}, indent=4)

    return output