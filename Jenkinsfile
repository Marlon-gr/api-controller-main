@Library(['aic-jenkins-sharedlib']) _

pythonBuildPipeline {

    // Use virgulas para enviar para mais de um canal ao mesmo tempo:
    // canalRocketChat = 'abc,xyz,meu_canal_prioritario'
    // Use um ID do RocketChat para enviar para usuarios:
    // canalRocketChat = 'abc,@f1234567.nome.sobrenome,def'

    canaisNotificacao = ''

    habilitarValidacaoPreReq        = true // habilita a validação dos pré-requisitos
    habilitarValidacaoEstatica      = false
    habilitarValidacaoSeguranca     = true // habilita a validação de segurança do código fonte
    habilitarConstrucao             = true // habilita a construção da aplicação
    habilitarTestesUnidade          = true // habilita a execução dos testes de unidade
    habilitarTestesIntegracao       = true // habilita a execução dos testes de integração
    habilitarTestesFumaca           = true // habilita a execução dos testes de fumaça
    habilitarSonar                  = false // habilita a execução do SonarQube Scanner
    habilitarEmpacotamento          = true // habilita o empacotamento da aplicação
    habilitarEmpacotamentoDocker    = true // habilita o empacotamento da aplicação
    habilitarPublicacao             = true // habilita a publicação do pacote no repositório corporativo
    habilitarDebug                  = false // habilita debug
}
