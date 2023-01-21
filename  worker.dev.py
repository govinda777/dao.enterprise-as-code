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

graph_attr = {
    "fontsize": "45",
    "color" : "red"
}

with Diagram("homolog", show=False, graph_attr=graph_attr, outformat=["jpg", "png", "dot"]):

    users = Users()
    mobileClient = MobileClient()
    client = Client()

    with Cluster("AWS VPN PRIVATE (Deia eu te amo, vou sentir muita saudade de quando vc estiver no Japão)"):

        newrelic = Newrelic()
        kong = Kong("API GW External")

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

            kong >> Edge(color=syncColor) >> elbOrder
            elbOrder >> Edge(color=syncColor) >> ec2MsOrder 
            ec2MsOrder >> Edge(color=syncColor) >> rdsPostgresOrder

            kong >> Edge(color=syncColor) >> elbBaseline
            elbBaseline >> Edge(color=syncColor) >> ec2MsBaseline 
            ec2MsBaseline >> Edge(color=syncColor) >> rdsPostgresBaseline

            kong >> Edge(color=syncColor) >> elbIdentity
            
            elbIdentity >> Edge(color=syncColor) >> ec2MsIdentity
            ec2MsIdentity >> Edge(color=syncColor) >> cognito 
