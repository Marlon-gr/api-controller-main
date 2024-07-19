from jaeger_client import Config
from flask_opentracing import FlaskTracing

def initialize_tracer():
    config = Config(
        config = {
            'sampler': {'type': 'const', 'param': 1}
        },
        service_name = 'api-controller'
    )
    return config.initialize_tracer()

def init_tracing(fapp):
    return FlaskTracing(initialize_tracer, True, fapp)