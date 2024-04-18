import requests


def session_for_src_addr(addr: str) -> requests.Session:
    """
    Create `Session` which will bind to the specified local address
    rather than auto-selecting it.
    """
    session = requests.Session()
    for prefix in ('http://', 'https://'):
        session.get_adapter(prefix).init_poolmanager(
            # those are default values from HTTPAdapter's constructor
            connections=requests.adapters.DEFAULT_POOLSIZE,
            maxsize=requests.adapters.DEFAULT_POOLSIZE,
            # This should be a tuple of (address, port). Port 0 means auto-selection.
            source_address=(addr, 0),
        )
    return session


def send_to_site(payload: dict) -> tuple:
    """
    This function sends requests to SiteApi
    """
    print('send to siteapi started')
    if payload is None:
        raise TypeError(f'Cannot send empty requests')
    print(type(payload))
    cert = ('svyatoslav.pem', 'svyatoslav.key', 'LqZLtJ')
    s = session_for_src_addr('10.72.240.155')  # binds requests session to specific interface
    res = s.post('http://10.233.10.68:3457/siteapi/schedule/order', json=payload, cert=cert)
    print('sended to siteapi started')
    return res.text, res.status_code


if __name__ == '__main__':
    payload = {"testDefinitionPath": '/Slava/RestApi/', "start": "", "priority": "normal",
               "testDefinitionParameters": [{"name": "kind", "value": "RestAPI_AS"}]}
    respose = send_to_site(payload=payload)
    print(respose)
    exit(0)
