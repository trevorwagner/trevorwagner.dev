import http.client

from urllib.parse import urlparse


def http_get(url):
    parser = urlparse(url)
    conn = http.client.HTTPSConnection(host=parser.hostname, port=parser.port)

    use_path = parser.path if parser.query is None else "{}?{}".format(parser.path, parser.query)

    conn.request(method="GET", url=use_path, headers={"Host": parser.hostname})
    response = conn.getresponse()

    return response.read().decode()
