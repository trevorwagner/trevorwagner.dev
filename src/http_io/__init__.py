import http.client

from urllib.parse import urlparse


def http_get(url):
    parser = urlparse(url)
    conn = http.client.HTTPSConnection(host=parser.hostname, port=parser.port)

    conn.request(method="GET", url=parser.path, headers={"Host": parser.hostname})
    response = conn.getresponse()

    return response
