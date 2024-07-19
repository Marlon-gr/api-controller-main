
FROM
ARG build_date
ARG vcs_reftrue
ARG VERSAO=1.0.0
ARG BOM_PATH="/docker"

RUN yum install -y gcc gcc-c++ make cmake python36-devel boost-devel libXext libSM libXrender
COPY dist/api_controller-1.0.0-py3-none-any.whl /
# hadolint ignore=DL3013
RUN pip3 install api_controller-1.0.0-py3-none-any.whl

RUN yum remove -y boost-devel gcc gcc-c++ make cmake

ENV VERSAO=$VERSAO \
    CMAKE_C_COMPILER=/usr/bin/gcc \
    CMAKE_CXX_COMPILER=/usr/bin/g++ \
    MODE=prod prometheus_multiproc_dir=/prometheus_multiproc

# Prometheus tmporal data.
RUN mkdir -p /prometheus_multiproc

EXPOSE 9000

WORKDIR /usr/local/lib/python3.6/site-packages/api_controller
# Save Bill of Materials to image. Não remova!
COPY README.md CHANGELOG.md LICENSE Dockerfile ${BOM_PATH}/

COPY api_controller/config ./config

# Run gunicorn
ENTRYPOINT ["gunicorn", "-c", "config/config.py", "--preload", "main:app"]