import json
import logging
import os


class ApiUtil:
    """
    Class that provides useful methods to be used in the project.
    """
    error_0 = 'face_compare_service->face_identify->(ApiUtil)-49 [' \
              'RequestException])'
    error_1 = 'face_compare_service->face_identify->(ApiUtil)-54' \
              ' [Similarity Response])'

    @staticmethod
    def get_url(env) -> str:
        """Prepare url.
        :param env: environment variable.
        :return: URL
        """
        url = None
        try:
            url = os.environ[env]
        except KeyError:
            logging.getLogger('controller.api').info('KeyErrorUrl: not found.')
        return url

    @staticmethod
    def logs(protocol, type_int, response, info):
        """Update the logs with the parameters received.
        :param protocol: ima protocol of the image.
        :param type_int: ima interface of the image (1 front, 2 verso).
        :param response: response of the request made.
        :param info: details of the operation performed
        """
        logging.getLogger('controller.api').info({
            'protocol': protocol,
            'type_interface': type_int,
            'response': response,
            'where': info,
        })

    def validate_post(self, post, err, msg, protocol, typ, api):
        """
        Validate response to the request made via POST.
        Args:
            post: (request) requisition response.
            err: (ResponseError) ResponseError class.
            msg: (requests.exceptions) Requisition error message.
            protocol: (str) Ima protocol (optional).
            typ: (int) Image interface type.
            api: (str) Endpoint with which the request was made (optional).
        """
        if post is False:
            status_code = 500
            response = err.raise_error_2(2, message=str(msg), status_code=500)
            self.logs(protocol, typ, str(msg), self.error_0)
        elif int(post.status_code) != 200:
            status_code = post.status_code
            self.logs(protocol, typ, str(post.text), self.error_1)
            response = err.raise_error_2(
                2, message=post.text + api, status_code=status_code)
        else:
            status_code = post.status_code
            response = json.loads(post.text)
        return response, status_code

    def validate_post_face_identify(self, post, err, msg, protocol, typ, api):
        if post is False:
            status_code = 500
            response = err.raise_error(2, message=str(msg), status_code=500)
            self.logs(protocol, typ, str(msg), self.error_0)
        elif int(post.status_code) != 200:
            status_code = post.status_code
            self.logs(protocol, typ, str(post.text), self.error_1)
            response = err.raise_error(
                2, message=post.text + api, status_code=status_code)
        else:
            status_code = post.status_code
            response = json.loads(post.text)
        return response, status_code

    @staticmethod
    def log_info(info):
        logging.getLogger('controller.api').info(info)
