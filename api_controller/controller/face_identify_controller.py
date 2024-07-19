from flask import Blueprint, jsonify, request

from api_controller.tracer import init_tracing
from api_controller.service.face_identify_service import \
    FaceIdentifyService
from api_controller.util.api_util import ApiUtil

face_identify = Blueprint('face_identify', __name__)
util = ApiUtil()
flask_tracer = init_tracing(face_identify)

@face_identify.route('/op3840078v1', methods=['POST'])
@flask_tracer.trace()
def check_probability_of_fraud():
    """Receive requisition via CURIO localhost:9000,
        process and return a response.
    """
    util.log_info("[ + ] INICIANDO ")
    util.log_info("-----------------START-----face_identify--------------")
    service = FaceIdentifyService('NEAREST_PERSON_FACE_IDENTIFY_URL')
    response, protocol, user_key, type_int = \
        service.start_face_identify_process(request)
    # Response for iib.
    output_response = {
        'codigoEstadoRetorno': int(response['code']),
        'listaIdentificacaoFraude': response['data'],
        'quantidadeListaIdentificacaoFraude': len(response['data']),
        'textoMensagemRetorno': str(response['message']),
        'codigoChaveFuncionario': user_key,
        'numeroProtocoloIdentificacaoImagem': int(protocol),
        'codigoTipoImagem': int(type_int)
    }

    util.log_info(f"[ + ] OBJETO DE RESPOSTA: {output_response}")
    util.log_info("[ + ] FINALIZANDO OPERAÇÃO ")

    return jsonify(output_response), 200
