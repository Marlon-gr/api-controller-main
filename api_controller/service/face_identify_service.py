import logging
import os

from api_controller.service.ima_service import ImaService
from api_controller.service.warehouse_service import WarehouseService
from api_controller.util.api_util import ApiUtil
from api_controller.util.request_util import RequestUtil
from api_controller.util.response_error import ResponseError


class FaceIdentifyService:
    """
    Definition of fraud identification services, integration with IBI.
    """
    url, user_key, protocol, type_int, base_64 = None, None, None, None, None
    file_type, file_size, requests = None, None, None
    str_e = " [SIMILARITY_FI]"
    error_2 = 'face_identify_service->face_identify->37 [unknown response])'

    def __init__(self, env_url):
        """
        Constructor of the class, declaration of attributes.
        """
        self.util = ApiUtil()
        self.error = ResponseError()
        self.url = self.util.get_url(env_url)

    def start_face_identify_process(self, request):
        """
        Start the fraud identification process.
        Obtain base64 from IMA.
        Start Integration with IBI.
        Args:
            request: (request) Object received in the request.
        Return:
            response (response) Request response object.
            protocol: (str) Ima protocol (optional).
            user_key: (str) User key.
            type_int: (int) Image interface.
        """
        self.util.log_info("[ + ] INCIANDO IDENTIFICACAO DE FRAUDE")
        result = request.get_json()
        self.user_key = result['codigoChaveFuncionario']
        self.protocol = result['numeroProtocoloIdentificacaoImagem']
        self.type_int = result['codigoTipoImagem']

        self.util.log_info(f"[ + ] CHAVE DE USUARIO RECEBIDA: {self.user_key}")
        self.util.log_info(f"[ + ] PROTOCOLO RECEBIDO: {self.protocol}")
        self.util.log_info(f"[ + ] TIPO DE IMAGEM RECEBIDO: {self.type_int}")

        # Ima base 64.
        self.util.log_info(f"[ + ] CONSTRUINDO OBJETO DE CONEXÃO COM IMA-CURIO")
        ima = ImaService(self.user_key, self.protocol, self.type_int)
        self.util.log_info(f"[ + ] URL DO IMA-CURIO: {self.util.get_url('IMA_CURIO_URL')}")

        self.file_type = ima.get_file_type()
        self.file_size = ima.get_file_size()
        ima_base64_response = ima.get_ima_b64()

        # Get Similarity-API response.
        if isinstance(ima_base64_response, dict):
            response = ima_base64_response
        else:  # Request Service Operation Start.
            self.base_64 = ima_base64_response
            self.__get_request()
            response = self.make_integration_ibi_service()
        # Return response.
        return response, self.protocol, self.user_key, self.type_int

    def make_integration_ibi_service(self):
        """
        Register base64 image for curation and begin integration with IBI.
        FACE IDENTIFY
        """
        # Register image in Warehouse Database.
        logging.getLogger('controller.api').info("[ + ] INICIANDO SERVICO DO WAREHOUSE")
        warehouse = WarehouseService('WAREHOUSE_ADD_IMAGE_URL')
        warehouse.register_image(
            self.base_64, self.protocol, self.type_int, self.file_type,
            self.file_size, "1")
        logging.getLogger('controller.api').info("[ + ] FINALIZANDO SERVICO DO WAREHOUSE")
        # Start face identify process.
        response = self.face_identify()
        return response

    def face_identify(self) -> dict:
        """Consume via rest the endpoint of Similarity->face-identify
            to identify if a face is in an image database (negative list, IIB).
        :return: response to the face-identify endpoint of the Similarity API.
        """
        response_post, error = self.requests.post(
            timeout=self.__get_timeout_nearest_person())
        # RequestException
        response_post, status_code = self.util.validate_post_face_identify(
            response_post, self.error, error, self.protocol, self.type_int,
            self.str_e)
        # Get response
        if status_code == 200:
            response_post = self.__get_response_data(response_post)
        return response_post

    def __get_request(self) -> None:
        """Prepare the request with the parameters.
        :return: Requests HTTP Library.
        """
        self.requests = RequestUtil({
            "b64_image": self.base_64,
            "protocol": self.protocol,
            "aligned_face": False
        }, self.url, self.str_e)

    @staticmethod
    def __get_response_data(response) -> dict:
        """Extract information from Similarity's response.
        :param response: response to the face-identify endpoint.
        :return: response for the REST operation.
        """
        output = {
            'code': 0,
            'data': [],
            'message': 'SUCCESS',
            'status_code': 200
        }
        for data in response['top_scores']:
            fraud = {
                'textoIdentificadorFotografiaFraude': str(data['name']),
                'valorProbabilidadeFraude': int(data['score'])
            }
            output['data'].append(fraud)
        return output

    @staticmethod
    def __get_timeout_nearest_person():
        """
        Timeout setting for nearest_person APY.
        """
        try:
            timeout_nearest_person = os.environ['TIMEOUT_NEAREST_PERSON']
        except KeyError:
            timeout_nearest_person = 25
        return float(timeout_nearest_person)

    def get_response_error(self, response_text, status_code):
        response_text = str(response_text) + self.str_e
        self.util.logs(self.protocol, self.type_int, response_text,
                       self.error_2)
        return self.error.raise_error(
            2, message=response_text, status_code=status_code)
