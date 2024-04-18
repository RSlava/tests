import requests
from urllib3.util.ssl_ import create_urllib3_context
from requests.adapters import HTTPAdapter


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        cert = ('svyatoslav.pem', 'svyatoslav.key', 'LqZLtJ')
        context = create_urllib3_context()
        context.load_cert_chain(certfile=cert[0], keyfile=cert[1], password=cert[2])
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)


def session_for_src_addr(addr: str) -> requests.Session:
    """
    Create `Session` which will bind to the specified local address
    rather than auto-selecting it.
    """
    session = requests.Session()
    session.verify = False  # If you don't want to validate server's public certificate
    session.mount("https://", SSLAdapter())
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
    s = session_for_src_addr('10.72.240.155')  # binds requests session to specific interface
    res = s.post('https://10.233.10.68:3457/siteapi/schedule/order', json=payload)
    print('sended to siteapi started')
    print(res.text, res.status_code)
    return res.text, res.status_code


if __name__ == '__main__':
    payload = {"testDefinitionPath": '/Slava/RestApi/', "start": "", "priority": "normal",
               "testDefinitionParameters": [{"name": "kind", "value": "RestAPI_AS"}]}
    respose = send_to_site(payload=payload)
    print(respose)
    exit(0)
