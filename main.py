from diagrams import Cluster, Diagram, Node, Edge
from diagrams.gcp.network import LoadBalancing
from diagrams.onprem.network import Kong
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDSPostgresqlInstance
from diagrams.aws.security import Cognito
from diagrams.aws.general import MobileClient
from diagrams.aws.general import Client
from diagrams.aws.general import Users
from diagrams.onprem.monitoring import Newrelic
from diagrams.aws.integration import SimpleQueueServiceSqsQueue
from diagrams.custom import Custom
from diagrams.programming.flowchart import Action
from diagrams.c4 import Person, Container, Relationship
from main_apiGw_external import MainApiGwExternal
from main_assincy import MainAssincy

objectve = """\
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to

    Arquitetura resiliente e adaptativa para
    trabalhar com transações Sincronas e 
    Assincronas.

    Possibilidades :

    Facilidade de criação de Workflows de processamento de Jornadas.

    Ex : Tela Rastreabilidade > Ação: Vincular fazenda > [Relatorio_ESG, Salvar_Dados_Base, Atualizacao_Auditoria]

    Obs : Entendo que nessa jornada o nosso usuário 
    não precisaria aguardar a execução do Relatorio_ESG.
    Poderiamos simplesmente agendar uma tarefa 
    e notifica-lo quando o mesmo for executado.

    ## Arquitetura orientada a Eventos : 

    Com uma arquitetura orientada a Eventos,
    teremos a possibilidade de que 
    quando algo for realizado pelo usuário
    a aplicação poderá apenas criar uma tarefa
    de atualização do relatório ESG por exemplo

    ## Qual será a nossa estatégia de gerendiamento
    de dados e comunidação na REDE MERX ?

    > * 
    > *
    > *

    Criar uma estratégia de comunidação entre
    toda as áreas do Software.

    ## API Gateway Deployment Model

    Utilizamos pouco a API Gw e suas funcionalidades, 

    Possibilidade de mandar a mesma mensagem 
    para 2 locais ao mesmo tempo.

    > ## Features API GW

    * Routing
    * API Orchestration
    * API Performance and Capacity Mgmt
    * Security, Identity and Access Mgmt
    * Protocol Translation
    * Analytics
    * Integration Layer (Connectivity / Messaging / Adapters)


    --> msg 
    --> --> Api Gw 
    --> --> --> [_] - Servicos_Sincronos 
    --> --> --> [_] - Servico_Assincronos
    --> --> --> [_] - Servicos_de_processamento_Geo_espacial
    --> --> --> --> --> - [Reques]
    --> --> --> --> --> - [Response]

    # API GW MERX

    ## [Responsabilidades]  

    * Realizar autenticação

        __ Jwt Authentication
        __ Basic Authentication

    * Encaminhamento de rotas

    >       __ Encaminhamento 1

          SERVIÇOS Sincrinos

    Atende chamadas que precisam ser
    atendidas online.

               > MS Identity (Assinatura de contratos)
               > MS Auditoria
               > MS Cobrança
               > MS Reports
               > ....

    >       __ Encaminhamento 2 

          Serviços Assincronos

    Atende chamadas que não possuem
    a necessidade de serem atendidas na mesma hora.

    Utiliza o sistema de filas, para organizar
    e gerenciar o processamento.

               > MS Order
               > MS Baseline
               > MS Identity

    >       __ Encaminhamento 3

          Serviços de Geo Processamento

    Atende chamadas que não possuem
    a necessidade de serem atendidas na mesma hora.

    Utiliza o sistema de filas, para organizar
    e gerenciar o processamento.

               > MS Order
               > MS Baseline
               > MS Identity


"""

graph_attr = {
    "fontsize": "45",
    "color" : "red"
}

with Diagram("main", show=False, graph_attr=graph_attr, outformat=["jpg", "png", "dot"]):

    users = Users()
    mobileClient = MobileClient()
    client = Client()
    
    with Cluster("AWS VPN PRIVATE (Deia eu te amo, vou sentir muita saudade de quando vc estiver no Japão)"):

        newrelic = Newrelic()
        kong = MainApiGwExternal("API GW External").connection
        
        apiOrquestrationDesc = Container(
                name="Orquestrador Requests",
                technology="Konga API GW",
                description="Script da manipulacao e gerenciamento das Requests",
        )

        apiScriptDesc = Container(
            name="Scripts Requests",
            technology="Konga API GW",
            description="Script da manipulacao e gerenciamento das Requests",
        )

        syncColor = "green"

        users >> Edge(color=syncColor) >> kong
        mobileClient >> Edge(color=syncColor) >> kong 
        client >> Edge(color=syncColor) >> kong
        
        with Cluster("API GW Development Model"):
            
            apiScript = Custom("Script route", "./img/api-gw-script.png")
            apiOrquestration = Custom("Orquestration", "./img/api-gw-orquestration.png")
            apiGw = [apiScript, apiOrquestration]
            
            kong >> Edge(color=syncColor) >> apiGw
            kong >> Edge(color=syncColor) >> apiGw
            apiOrquestrationDesc >> Edge(color=syncColor) >> apiOrquestration
            apiScriptDesc >> Edge(color=syncColor) >> apiScript
            
        with Cluster("SYNCHRONOUS Services"):

            elbOrder = LoadBalancing("Balance Order")
            elbBaseline = LoadBalancing("Balance Baseline")
            elbIdentity = LoadBalancing("Balance Identity")

            with Cluster("MS Order"):
                ec2MsOrder = EC2("Order Java 8")
                
                with Cluster("Postgres Order"):
                    rdsPostgresOrder = RDSPostgresqlInstance("RDS")

            with Cluster("MS Baseline"):
                ec2MsBaseline = EC2("Baseline Java 8")
                
                with Cluster("Postgres Baseline"):
                    rdsPostgresBaseline = RDSPostgresqlInstance("RDS")

            with Cluster("MS Identity"):
                ec2MsIdentity = EC2("Identity Java 8")
                cognito = Cognito("Cognito")

            syncColor = "green"

            apiOrquestration >> Edge(color=syncColor) >> elbOrder
            elbOrder >> Edge(color=syncColor) >> ec2MsOrder 
            ec2MsOrder >> Edge(color=syncColor) >> rdsPostgresOrder

            apiOrquestration >> Edge(color=syncColor) >> elbBaseline
            elbBaseline >> Edge(color=syncColor) >> ec2MsBaseline 
            ec2MsBaseline >> Edge(color=syncColor) >> rdsPostgresBaseline

            apiOrquestration >> Edge(color=syncColor) >> elbIdentity
            
            elbIdentity >> Edge(color=syncColor) >> ec2MsIdentity
            ec2MsIdentity >> Edge(color=syncColor) >> cognito  

        with Cluster("ASYNCHRONOUS 11111 SERVICES"):
            
            mainAssincy = MainAssincy("Serviços asyscronos requerem arquiteturas especificas")
                
            programa = """
            title="Serviços asyscronos requerem arquiteturas especificas para o tratamento e gerenciamneto dos EVENTOS"
            necessidades_diferenciais=["Tratamento_de_mensagens", "Processamento_por_Jobs", "Filas_de_reprocessamento", "Garantia_de_resposta"]


            for item in necessidades_diferenciais:
                webapp = Container(
                    name="Web Application",
                    technology="Java and Spring MVC",
                    description="Delivers the static content and the Internet banking single page application.",
                )
            """

            apiGw >> Edge(color=syncColor) >> mainAssincy.connection

            

        
        