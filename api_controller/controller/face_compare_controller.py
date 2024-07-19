import logging

from flask import Blueprint, jsonify, request
from api_controller.tracer import init_tracing

from api_controller.service.face_compare_service import \
    FaceCompareService
from api_controller.service.ima_service import ImaService

face_compare = Blueprint('face_compare', __name__)
flask_tracer = init_tracing(face_compare)

@face_compare.route('/op3852047v1', methods=['POST'])
@flask_tracer.trace()
def check_similarity_between_images():
    """Receive requisition via CURIO localhost:9000,
        process and return a response.
    """
    logging.getLogger('controller.api').info(
        "-----------------START----op3852047v1-----face_compare"
        "-----------------START----op3852047v1-----face_compare--------------")
    result = request.get_json()
    user_key = result['codigoChaveFuncionario']
    pr_photo = result['numeroProtocoloIdentificacaoImagemFoto']
    pr_docum = result['numeroProtocoloIdentificacaoImagemDocumento']
    co_photo = result['codigoTipoImagemFoto']
    co_docum = result['codigoTipoImagemDocumento']
    # Get protocol and interface.
    protocol = str(pr_photo) + " <F-D> " + str(pr_docum)
    type_interface = str(co_photo) + " <F-D> " + str(co_docum)
    # Get Base64 from IMA.
    ima_photo = ImaService(user_key, pr_photo, co_photo)
    base64_photo = ima_photo.get_ima_b64()
    ima_photo = ImaService(user_key, pr_docum, co_docum)
    base64_docum = ima_photo.get_ima_b64()
    # Get Similarity-API response.
    if isinstance(base64_photo, dict):
        s_response = base64_photo
    elif isinstance(base64_docum, dict):
        s_response = base64_docum
    else:
        similarity = FaceCompareService(
            base64_photo, base64_docum, 'SIMILARITY_FACE_COMPARE_URL')
        s_response = similarity.face_compare(protocol, type_interface)
    # response for iib.
    output_response = {
        'codigoEstadoRetorno': s_response['code'],
        'textoMensagemRetorno': s_response['message'],
        'codigoChaveFuncionario': user_key,
        'numeroProtocoloIdentificacaoImagemFoto': int(pr_photo),
        'numeroProtocoloIdentificacaoImagemDocumento': int(pr_docum),
        'codigoTipoImagemFoto': int(co_photo),
        'codigoTipoImagemDocumento': int(co_docum),
        'textoIdentificadorFoto': '',
        'textoIdentificadorDocumento': '',
        'indicadorSimilaridade': s_response['identical'],
        'valorProbabilidadeSimilaridade': s_response['confidence']
    }
    logging.getLogger('controller.api').info(output_response)
    logging.getLogger('controller.api').info(
        "------------------END----op3852047v1-----face_compare"
        "------------------END----op3852047v1-----face_compare---------------")
    return jsonify(output_response), 200
