import http.client

from urllib.parse import urlparse


def get_remote_data(url):
    parser = urlparse(url)
    conn = http.client.HTTPSConnection(host=parser.hostname, port=parser.port)

    conn.request(method="GET", url=parser.path, headers={"Host": parser.hostname})
    response = conn.getresponse()

    body = response.read().decode()

    return body
