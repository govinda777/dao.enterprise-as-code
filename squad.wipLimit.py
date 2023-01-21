from diagrams import Cluster, Diagram, Node, Edge
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Deployment, Pod, ReplicaSet
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.podconfig import ConfigMap, Secret
from diagrams.k8s.compute import Deploy
from diagrams.aws.compute import EC2ContainerRegistry
from diagrams.k8s.clusterconfig import HorizontalPodAutoscaler
from diagrams.c4 import Person, Container, Database, System, SystemBoundary, Relationship


with Diagram("eks.cluster", show=False):

    with Cluster("labels > app_name-service"):

        service = Service("app_name-service")            

        with Cluster("labels > app_name-api-ingress / deploy"):

            ingress = Ingress("app_name.com") 

            deployment = Deployment()

            horizontalPodAutoscaler = HorizontalPodAutoscaler("Horizontal Pod Auto scaler")
            
            service >> deployment
            service >> ingress
            service >> horizontalPodAutoscaler

            with Cluster("labels > app_name-api"):
                
                pod = Pod("app_name_pod")
                configMap = ConfigMap("app_name-configmap")
                secret = Secret("app_name.jasypt")
                image = EC2ContainerRegistry("Docker Image ECR")

                ingress >> pod
                deployment >> pod
                horizontalPodAutoscaler >> pod

                pod >> image
                pod >> secret
                pod >> configMap
