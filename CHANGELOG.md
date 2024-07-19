# Changelog

Todas as mudanças notáveis serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](http://keepachangelog.com/pt-BR/1.0.0/) e este projeto adere ao padrão [Semantic Versioning](http://semver.org/lang/pt-BR/spec/v2.0.0.html).

## [Não liberado]
### Adicionado
### Corrigido
### Modificado
### Obsoleto
### Removido

## [0.2.73](api-controller/tags/0.2.73) - 2020-10-15
### Removido
    - Remove custom prometheus metrics.
    
## [0.2.72](api-controller/tags/0.2.72) - 2020-10-07
### Adicionado
    - ERRO -> api_controller/service/ima_service.py", line 53, in get_ima_b64

## [0.2.66](api-controller/tags/0.2.66) - 2020-09-24
### Adicionado
    - Metrics for protocol
    
## [0.2.52](api-controller/tags/0.2.52) - 2020-09-04
### Modificado    
    - Erro reparando erro de código.
    - Update Docker file.
    
## [0.2.42](api-controller/tags/0.2.42) - 2020-09-02
### Modificado    
    - Gunicorn configuration.
    - Update Docker file.
    
## [0.2.3](api-controller/tags/0.2.3) - 2020-09-01
### Corrigido
    - Metrics to the application.

## [0.2.2](api-controller/tags/0.2.2) - 2020-08-31
### Adicionado
    - Metrics to the application.
    - Documentation of the classes and methods.
    - Integration with Nearest_Person API.
### Modificado
    - Error handling and response for IMA.
    - Gunicorn configuration.
    - Update Docker file.
    
## [0.2.0](api-controller/tags/0.2.0) - 2020-08-06
### Adicionado
    - Timeout for env similarity.
     
## [0.1.9](api-controller/tags/0.1.4) - 2020-07-24
### Corrigido
    - Error 'indicadorSimilaridade': s_response['identical'], KeyError
    : 'identical'. Ocorreu um erro quando a integração com a API IMA-CURIO
     não retorna a base 64.
    
## [0.1.8](api-controller/tags/0.1.3) - 2020-07-16
### ADICIONADO
    - Integração com warehouse no serviço de checagem de probabilidade de fraude

## [0.1.7](api-controller/tags/0.1.3) - 2020-07-15
### ADICIONADO
    - Logs nos fluxos das controllers

## [0.1.4](api-controller/tags/0.1.3) - 2020-05-14
### ADICIONADO
    - Envio de imagem para o warehouse.

## [0.1.3](api-controller/tags/0.1.3) - 2020-05-14
### Modificado
    - Alteração do código de resposta de 200 para 0.

## [0.1.2](api-controller/tags/0.1.2) - 2020-03-18
### Modificado
    - Adição de parâmetro de protocolo para o face-similarity.

## [0.1.1](api-controller/tags/0.1.1) - 2020-02-21
### Modificado
    - Elimanada chamada da API IMA paralelemente, por erro.

## [0.1.0](api-controller/tags/0.1.0) - 2020-02-12
Versão inicial
### Adicionado
    - Servidor uwsgi para produção.
    - Servidor werkzeug para desenvolvimento.
    - Testes unitários da API de controller.
    - Logging para /var/log/controller* e /var/log/uwsgi*.
    - Documentção Swagger.
    - endpoint face-detect.
    - endpoint face-identify.
    - endpoint face-compare.
    - documentação do codigo.
### Modificado
    - Update Docker file and enable empacotamento Docker no Jenkinsfile.