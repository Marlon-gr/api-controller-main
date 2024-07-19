import logging

from flask import Blueprint, jsonify, request
from api_controller.tracer import init_tracing

from api_controller.service.face_detect_service import FaceDetectService
from api_controller.service.ima_service import ImaService

face_detect = Blueprint('face_detect', __name__)
flask_tracer = init_tracing(face_detect)

@face_detect.route('/op3839030v1', methods=['POST'])
@flask_tracer.trace()
def check_for_face_in_the_image():
    """Receive requisition via CURIO localhost:9000,
        process and return a response.
    """
    logging.getLogger('controller.api').info(
        "-----------------START----op3839030v1-----face_detect"
        "-----------------START----op3839030v1-----face_detect---------------")
    result = request.get_json()
    user_key = result['codigoChaveFuncionario']
    protocol = result['numeroProtocoloIdentificacaoImagem']
    type_int = result['codigoTipoImagem']
    # Get base64 from IMA.
    ima = ImaService(user_key, protocol, type_int)
    ima.set_tracer(flask_tracer, flask_tracer.get_span(request))
    base_64 = ima.get_ima_b64()
    # Get Similarity-API response.
    if isinstance(base_64, dict):
        s_response = base_64
    else:
        # Similarity operation.
        similarity = FaceDetectService(base_64, 'SIMILARITY_FACE_DETECT_URL')
        similarity.set_tracer(flask_tracer, flask_tracer.get_span(request))
        s_response = similarity.face_detect(protocol, type_int)
    # Response for iib.
    with flask_tracer.tracer.start_active_span('Return Parsing'):
        output_response = {
            'codigoEstadoRetorno': int(s_response['code']),
            'listaIdentificacaoPessoa': s_response['data'],
            'quantidadeListaIdentificacaoPessoa': int(len(s_response['data'])),
            'textoMensagemRetorno': s_response['message'],
            'codigoChaveFuncionario': user_key,
            'numeroProtocoloIdentificacaoImagem': int(protocol),
            'codigoTipoImagem': int(type_int)
        }
    logging.getLogger('controller.api').info(output_response)
    logging.getLogger('controller.api').info(
        "------------------END----op3839030v1-----face_detect"
        "------------------END----op3839030v1-----face_detect----------------")
    return jsonify(output_response), 200
