import json

from api_controller.util.api_util import ApiUtil
from api_controller.util.request_util import RequestUtil
from api_controller.util.response_error import ResponseError


class ImaService:

    __b64_image = None
    util = ApiUtil()
    error = ResponseError()

    str_e = " [IMA]"
    error_0 = 'ima_service->get_ima_b64->55 [IMA Response])'

    def __init__(self, user_key, protocol, type_interface):
        """
        Constructor of the class, declaration of attributes.
        """
        self.protocol = protocol
        self.user_key = user_key
        self.type_int = type_interface
        self.file_type = None
        self.file_size = None
        # Init Request
        self.requests = RequestUtil(self.__payload(
            user_key, protocol, type_interface
        ), self.util.get_url('IMA_CURIO_URL'), api=self.str_e)

    def set_tracer(self, tracer, base_span):
        self.tracer = tracer    
        self.tracer_base_span = base_span

    @staticmethod
    def __payload(user_key, protocol, type_interface) -> dict:
        """Prepare the payload for the requisition.
        :param user_key: user key of the .
        :param protocol: ima protocol of the image.
        :param type_interface: ima interface of the image (1 front, 2 verso).
        :return: payload.
        """
        payload = {
            "chave_usuario": user_key,
            "protocolo_imagem": protocol,
            "tipo_imagem": [type_interface]
        }
        return payload

    def get_ima_b64(self) -> str or dict:
        """
        Extract information from IMA response.
        :return: base 64 for the REST operation.
        """
        self.util.log_info("[ + ] INICIANDO REQUISIÇÃO PARA IMA-CURIO")
        with self.tracer.tracer.start_span('Get IMA Curio Image', child_of=self.tracer_base_span) as span:
            span.set_tag('ProtocoloIMA', self.protocol)
            response, error = self.requests.post()
            if response is False:
                return self.error.raise_error(1, message=error)
            # IMA response load.
            ima_response = json.loads(response.text)
            try:
                self.file_type = ima_response[0]['nomeExtensao']
                self.file_size = ima_response[0]['numeroTamanhoImagem']
                self.util.log_info(f"[ + ] EXTENSÃO DA IMAGEM RECEBIDA: {self.file_type}")
                self.util.log_info(f"[ + ] TAMANHO DA IMAGEM RECEBIDA: {self.file_size}")
                output = ima_response[0]['imagemBinario']
            except KeyError:
                output = self.error.raise_error(1, response.text + self.str_e)
                self.util.logs(
                    self.protocol, self.type_int, ima_response, self.error_0)
            return output

    def get_file_type(self):
        """
        Get file type from base64.
        """
        return self.file_type

    def get_file_size(self):
        """
        Get file size from base64.
        """
        return self.file_size
