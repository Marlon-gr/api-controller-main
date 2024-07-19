import json
import logging
import urllib.request

import requests


class RequestUtil:

    header_json = {'content-type': 'application/json'}

    def __init__(self, payload, url, api=None):
        self.url = url
        self.payload = payload
        self.__api = api

    def post(self, verify=False, timeout=25):
        """Sends a POST request.
        :param verify:  Either a boolean, in which case it controls whether
                        we verify the server's TLS certificate.
        :param timeout: (optional) How many seconds to wait for the server to
                        send data before giving up.
        :return: <Response> object
        """
        try:
            proxies = self.__get_proxies(self.url)
            response = requests.post(
                url=self.url, data=json.dumps(self.payload),
                headers=self.header_json, verify=verify,
                timeout=timeout, proxies=proxies
            )
            error = None
        except requests.exceptions.ReadTimeout as e:
            response, error = self.timeout_exception(self.__api, e)
        except requests.exceptions.RequestException as e:
            response, error = self.timeout_exception(self.__api, e)
        return response, error

    @staticmethod
    def timeout_exception(api, error):
        """
        Timeout error, exception handling.
        For Warehouse API I do nothing I just continue.
        Args:
            api (bool): Check if the requisition is for warehouse API.
            error (ReadTimeout): Error returned by the exception (ReadTimeout).
        """
        response = False
        error = str(error) + str(api)
        if api == "WAREHOUSE":
            # Timeout = 0.0000000001, fire and forget response.
            pass
        else:
            logging.getLogger('controller.request').info(error)
        return response, error

    @staticmethod
    def __get_proxies(url):
        """
        Obtain a proxy from the operational system if necessary.
        (in case of using VPN with the bank it is necessary to use the proxy)
        Args:
            url: (str) Endpoint with which the request was made.
        Returns:
            (str) Proxy url.
        """
        if "127.0.0.1" in url or "0.0.0.0" in url or "localhost" in url:
            proxies = {"http": "", "https": ""}
        else:
            http = urllib.request.getproxies().get("http")
            https = urllib.request.getproxies().get("https")
            proxies = {"http": http, "https": https}
        return proxies
