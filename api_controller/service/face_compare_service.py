import os

from api_controller.util.api_util import ApiUtil
from api_controller.util.request_util import RequestUtil
from api_controller.util.response_error import ResponseError


class FaceCompareService:
    """
    Definition of facial comparison services.
    """
    __url = None
    __b64_image_1 = None
    __b64_image_2 = None
    util = ApiUtil()
    error = ResponseError()

    str_e = " [SIMILARITY_FC]"
    error_2 = 'face_compare_service->face_compare->47 [unknown response])'

    def __init__(self, b64_image_1, b64_image_2, env_url):
        """
        Constructor of the class, declaration of attributes.
        """
        self.__b64_image_1 = b64_image_1
        self.__b64_image_2 = b64_image_2
        self.__url = self.util.get_url(env_url)
        self.__get_request()

    def face_compare(self, protocol, type_int) -> dict:
        """Consume via rest the endpoint of Similarity->face-compare to
        compare the faces of two images and find the distance between them
        :param protocol: ima protocol of the image.
        :param type_int: ima interface of the image (1 front, 2 verso).
        :return: response to the face-compare endpoint of the Similarity API.
        """
        response_post, error = self.requests.post()
        # RequestException
        response_post, status_code = self.util.validate_post(
            response_post, self.error, error, protocol, type_int, self.str_e)
        # Get response.
        if status_code == 200:
            response_post = self.__get_response_data(response_post)
        return response_post

    def __get_request(self) -> None:
        """Prepare the request with the parameters.
        :return: Requests HTTP Library.
        """
        self.requests = RequestUtil({
            "img1": self.__b64_image_1,
            "img2": self.__b64_image_2
        }, self.__url, self.str_e)

    @staticmethod
    def __get_response_data(response) -> dict:
        """Extract information from Similarity's response.
        :param response: response to the face-compare endpoint.
        :return: response for the REST operation.
        """
        if float(response['similarity']) >= float(70):
            similarity = "S"
        else:
            similarity = "N"
        output = {
            'code': 0,
            'identical': similarity,
            'confidence': float(response['similarity']),
            'message': 'Operação executada com sucesso'
        }
        return output

    @staticmethod
    def get_timeout_similarity():
        """
        Timeout setting for nearest_person APY.
        """
        try:
            timeout_similarity = os.environ['TIMEOUT_NEAREST_PERSON']
        except KeyError:
            timeout_similarity = 25
        return float(timeout_similarity)

    def get_response_error(self, protocol, type_int, response_text):
        response_text = response_text + self.str_e
        self.util.logs(protocol, type_int, response_text, self.error_2)
        return self.error.raise_error_2(2, message=response_text)
