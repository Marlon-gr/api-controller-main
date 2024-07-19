from flask import Blueprint
from api_controller.tracer import init_tracing

start = Blueprint('start', __name__)
flask_tracer = init_tracing(start)

@start.route('/')
def index():
    """Welcome to  Controller API."""
    return 'Welcome to  Controller API, read documentation in /docs ' \
           'for further questions.', 200


@start.route('/health', methods=['GET'])
@flask_tracer.trace()
def health():
    """Endpoint used by CURIO to know if the API is standing"""
    return "Up", 200
