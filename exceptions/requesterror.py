import requests


class RequestError(Exception):
    def __init__(self, request: requests.Response, msg: str = None):
        if msg is None:
            msg = "An error occured making the following request: {}".format(request.url)
        super(RequestError, self).__init__(msg)
        self.request = request
