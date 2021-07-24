import requests
import json

params = {
    "grant_type": "password",
    "client_id": "3MVG9fe4g9fhX0E5jSHLvn.5q0v1DuKleC3AUWEIfv6PQpg52TB0rrDyzyj.e8PJdqEraCubfdnyOgeTDErsn", # Consumer Key
    "client_secret": "624C34779AFFA5BB49852FF53B23881FBAED3F1ED718D873EA27BFA8FFEC8B30", # Consumer Secret
    "username": "abhishek@96.com", # The email you use to login
    "password": "s2pu6VAaph9HM5pQP1RAO24qwgnCD8ZetPUHczE" # Concat your password and your security token
}
r = requests.post("https://login.salesforce.com/services/oauth2/token", params=params)
# if you connect to a Sandbox, use test.salesforce.com instead
access_token = r.json().get("access_token")
instance_url = r.json().get("instance_url")
print("Access Token:", access_token)
print("Instance URL", instance_url)


def sf_api_call(action, parameters = {}, method = 'get', data = {}):
    """
    Helper function to make calls to Salesforce REST API.
    Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
    """
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
    }
    if method == 'get':
        r = requests.request(method, instance_url+action, headers=headers, params=parameters, timeout=30)
    elif method in ['post', 'patch']:
        r = requests.request(method, instance_url+action, headers=headers, json=data, params=parameters, timeout=10)
    else:
        # other methods not implemented in this example
        raise ValueError('Method should be get or post or patch.')
    print('Debug: API %s call: %s' % (method, r.url) )
    if r.status_code < 300:
        if method=='patch':
            return None
        else:
            return r.json()
    else:
        raise Exception('API error when calling %s : %s' % (r.url, r.content))


print(json.dumps(sf_api_call('/services/data/v52.0/query/', {
    'q': 'SELECT  Name, Phone from Account'
}), indent=2))
