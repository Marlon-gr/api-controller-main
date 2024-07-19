import json

from api_controller.util.api_util import ApiUtil
from api_controller.util.request_util import RequestUtil
from api_controller.util.response_error import ResponseError


class FaceDetectService:
    """
    Definition of facial detection services.
    """
    __url = None
    __b64_image = None
    util = ApiUtil()
    error = ResponseError()

    str_e = " [SIMILARITY_FD]"
    error_0 = 'face_detect_service->face_detect->28 [RequestException])'
    error_1 = 'face_detect_service->face_detect->52 [Similarity Response])'
    error_2 = 'face_detect_service->face_detect->36 [unknown response])'

    def __init__(self, b64_image, env_url):
        """
        Constructor of the class, declaration of attributes.
        """
        self.base_64 = b64_image
        self.__url = self.util.get_url(env_url)
        self.__get_request()

    def face_detect(self, protocol, type_int):
        """Consume via rest the endpoint of Similarity->face-detect
            to extract faces from the image.
        :param protocol: ima protocol of the image.
        :param type_int: ima interface of the image (1 front, 2 verso).
        :return: response to the face-detect endpoint of the Similarity API.
        """
        with self.tracer.tracer.start_span('Face Detect Request', child_of=self.tracer_base_span) as span:
            span.set_tag('ProtocoloIMA', protocol)
            response_post, error = self.requests.post()
            if response_post is False:
                response = self.error.raise_error(2, message=error)
                self.util.logs(protocol, type_int, response, self.error_0)
                return response
            # get response
            response_text = json.loads(response_post.text)
            # is response valid.
            if "code" in response_text and "data" in response_text:
                response = self.__get_response_data(
                    response_text, protocol, type_int, response_post.text)
            else:
                self.util.logs(protocol, type_int, response_text, self.error_2)
                response = self.error.raise_error(
                    2, message=response_post.text + self.str_e)
            return response

    def set_tracer(self, tracer, base_span):
        self.tracer = tracer    
        self.tracer_base_span = base_span

    def __get_request(self) -> None:
        """Prepare the request with the parameters.
        :return: Requests HTTP Library.
        """
        self.requests = RequestUtil(
            self.__payload(self.base_64), self.__url, api=self.str_e)

    @staticmethod
    def __payload(b64_image) -> dict:
        """Prepare the payload for the requisition.
        :param b64_image: string base64 image.
        :return: payload.
        """
        payload = {
            "b64_image": b64_image,
        }
        return payload

    def __get_response_data(self, response, protocol, type_int, text) -> dict:
        """Extract information from Similarity's response.
        :param response: response to the face-detect endpoint.
        :return: response for the REST operation.
        """
        if int(response['code']) != 200:
            self.util.logs(protocol, type_int, response, self.error_1)
            response = self.error.raise_error(2, message=text + self.str_e)
        else:
            faces = []
            for data in response['data']:
                face = {
                    'textoIdentificadorFotografia': str(data['id']),
                    'indicadorIdadePessoa': int(data['idade']),
                    'indicadorSexoPessoa': str(data['sexo']).upper()
                }
                faces.append(face)
            response['code'] = 0
            response['data'] = faces
        return response
