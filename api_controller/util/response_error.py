

class ResponseError:
    """
    Class that implements methods to treat the responses received
    from the requisitions. (Error handling)
    """

    error_dict = {
        0: "Operação executada com sucesso",
        1: "Imagem não encontrada",
        2: "Erro ao processar a operação"
    }

    def raise_error(self, code, message=None, status_code=None):
        """Prepare error response for or IIB.
        :param code: error code.
        :param message: Return message for curio.
        :param status_code: Status code from request.
        :return: Response error
        """
        output = {
            'code': code,
            'data': [],
            'identical': "N",
            'confidence': float(0),
            'message': str(self.get_message(code, message)),
            'status_code': status_code
        }
        return output

    def raise_error_2(self, code, message=None, status_code=None):
        """Prepare error response for or IIB. For face-compare.
        :param code: error code.
        :param status_code: Status code from request.
        :param message: Return message for curio.
        :return: Response error
        """
        output = {
            'code': code,
            'identical': "N",
            'confidence': float(0),
            'message': str(self.get_message(code, message)),
            'status_code': status_code
        }
        return output

    def get_message(self, code, message):
        """
        Get requisition message.
        Args:
            code (int): Response status code.
            message (str) Requisition error message.
        """
        if message is None:
            text = self.error_dict.get(code, None)
        else:
            text = message
        return text
