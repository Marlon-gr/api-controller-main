
from api_controller.util.api_util import ApiUtil
from api_controller.util.request_util import RequestUtil
from api_controller.util.response_error import ResponseError


class WarehouseService:
    """
    Class to perform integration with the API warehouse and register images.
    """
    __url = None
    util = ApiUtil()
    error = ResponseError()

    def __init__(self, env):
        """
        Class Constructor.
        """
        self.__url = self.util.get_url(env)

    def register_image(self, base_64, protocol, type_int, file_type,
                       file_size, source):
        """
        Add image in Warehouse Data Base.
        Warehouse API integration.
        Args:
            base_64: (str) image base64.
            protocol: (str) IMA imaging protocol.
            type_int: (int) Image interface.
            file_type: (str) File type (JPG, PNG, etc..).
            file_size: (int) File size.
            source: (int) Source from base64.
        """
        self.util.log_info(f"[ + ] PAYLOAD:")
        self.util.log_info(f"[ + ] PROTOCOLO: {protocol}")
        self.util.log_info(f"[ + ] TIPO DE IMAGEM: {type_int}")
        self.util.log_info(f"[ + ] EXTENSAO DO ARQUIVO: {file_type}")
        self.util.log_info(f"[ + ] TAMANHO DO ARQUIVO: {file_size}")
        self.util.log_info(f"[ + ] CODIGO DE ORIGEM: {source}")

        payload = {
            'base_64': base_64,
            'protocolo': str(protocol),
            'num_interface': type_int,
            'extensao': file_type,
            'tamanho_imagem': file_size,
            'origem': source
        }
        service = RequestUtil(payload, self.__url, api="WAREHOUSE")
        service.post(verify=False, timeout=0.000000001)
