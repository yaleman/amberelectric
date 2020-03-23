""" does the thing what connects to stuff """

import json
import requests
import requests.exceptions

URLS = {
    'auth' : "https://api-bff.amberelectric.com.au/api/v1.0/Authentication/SignIn",
    'prices' : 'https://api-bff.amberelectric.com.au/api/v1.0/Price/GetPriceList',
    'getusage' : 'https://api-bff.amberelectric.com.au/api/v1.0/UsageHub/GetUsageForHub',
}

class AmberElectric():
    """ basic API thingie for pulling data from the Amber Electric APIs """
    def __init__(self, username=None, password=None):
        """ do startup things """
        if username:
            self.username = username
        if password:
            self.password = password
        if username and password:
            self.auth()
        else:
            self.username = self.password = False
            self.tokens = {}

    def set_auth_or_raise(self, username=None, password=None):
        """ sets the internal username and/or password values, and raises a ValueError if they're not set """
        if not username and not self.username:
            raise ValueError("No username specified")
        if not password and not self.password:
            raise ValueError("No password specified")

        if username:
            self.username = username
        if password:
            self.password = password

    def auth(self, auth_username=None, auth_password=None):
        """ connects and sets the token

        example response from the API:
        {
        "data": {
            "name": "John Citizen",
            "firstName": null,
            "lastName": null,
            "postcode": "1000",
            "email": "user@example.com",
            "idToken": "<jwt>",
            "refreshToken": "<jwt>"
        },
        "serviceResponseType": 1,
        "message": "Authentication successfully."
        }

        """
        self.set_auth_or_raise(auth_username, auth_password)

        # try the login thing

        headers = {
            'content-type' : 'application/json',
            'accept' : 'application/json',
            'authority' : 'api-bff.amberelectric.com.au',
            'origin' : 'https://app.amberelectric.com.au',
            'accept-language' : 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        data = {
            'username' : self.username,
            'password' : self.password,
        }
        try:
            response = requests.post(URLS['auth'], headers=headers, data=json.dumps(data))
            response.raise_for_status()
        except requests.exceptions.HTTPError as httperror:
            print(f"dir(httperror):\n{dir(httperror)})")
            print(f"response:\n{response})")
            print(f"dir(response):\n{dir(response)}")
            print(f"response.request:\n{response.request.headers}")
        jsondata = response.json()
        if not jsondata.get('serviceResponseType') == 1:
            raise Exception(f"Um, error? {json.dumps(jsondata, indent=4)}")
        elif not jsondata.get('data'):
            raise Exception(f"Um, error? {json.dumps(jsondata,indent=4)}")

        self.tokens = {
            'refreshtoken' : jsondata.get('data', {}).get('refreshToken'),
            'idtoken' : jsondata.get('data', {}).get('idToken'),
        }
        self.userinfo = {
            "name": jsondata.get('name',""),
            "firstname": jsondata.get('firstName',""),
            "lastname": jsondata.get('lastName',""),
            "postcode": jsondata.get('postcode',""),
            "email": jsondata.get('email',""),
        }
        return True


    def getpricelist(self, ):
        """ pulls the pricelist """
        if not self.tokens:
            self.auth()
        headers = {
            'refreshtoken' : self.tokens.get('refreshtoken'),
            'authorization' : self.tokens.get('idtoken'),
        }
        data = {}
        try:
            response = requests.post(URLS['prices'], headers=headers, data=data)
            response.raise_for_status()
            jsondata = response.json()
        except requests.exceptions.HTTPError as httperror:
            print(f"dir(httperror):\n{dir(httperror)})")
            print(f"response:\n{response})")
            print(f"dir(response):\n{dir(response)}")
            print(f"response.request:\n{response.request.headers}")
        if not response.json().get('serviceResponseType') == 1:
            raise Exception(f"Um, error? {json.dumps(jsondata, indent=4)}")
        return jsondata.get('data')
        #'origin: https://app.amberelectric.com.au'
        # 'authority: api-bff.amberelectric.com.au'
        #  'pragma: no-cache'
        #  'cache-control: no-cache'
        #  'refreshtoken: <jwt>'
        #  'authorization: <jwt>'
        #  'content-type: application/json'
        #  'accept: application/json'
        #  'sec-fetch-dest: empty'
        #  'sec-fetch-site: same-site'
        #  'sec-fetch-mode: cors'
        #  'referer: https://app.amberelectric.com.au/live-price'
        #  'accept-language: en-GB,en-US;q=0.9,en;q=0.8'
        # --data-binary '{"headers":{"normalizedNames":{},"lazyUpdate":null,"headers":{}}}' --compressed

    def getusage(self):
        """ grabs the usage data """

        # fetch("", {"credentials":"include",
        headers = {
            "accept":"application/json",
            "accept-language":"en-GB,en-US;q=0.9,en;q=0.8",
            "authorization": self.tokens.get('idtoken'),
            "cache-control":"no-cache",
            "content-type":"application/json",
            "pragma":"no-cache",
            "refreshtoken": self.tokens.get('refreshToken'),
        }
        data = {
            "headers": {
                "normalizedNames" : {},
                "lazyUpdate" : "",
                "headers ": {}
            }
        }
        response = requests.post(URLS['getusage'], headers=headers, data=data)
        response.raise_for_status()
        return response.json().get('data')

        #,"sec-fetch-dest":"empty","sec-fetch-mode":"cors","sec-fetch-site":"same-site"},
        # "referrer":"https://app.amberelectric.com.au/usage/anytime",
        # "referrerPolicy":"no-referrer-when-downgrade",
        # "body":"{\"headers\":{\"normalizedNames\":{},\"lazyUpdate\":null,
        #       \"headers\":{}}}","method":"POST","mode":"cors"});
