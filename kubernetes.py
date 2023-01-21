from diagrams import Diagram
from diagrams.onprem.network import Kong
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Deployment, Pod, ReplicaSet
from diagrams.k8s.network import Ingress, Service

class Kubernetes:

    def __init__(self, name):
        self._name = name
        self._other = "foo"
        self._connection = Kong("API GW Internal")
        self.exec()
    
    @property
    def title(self):
        return self._name
    
    @property
    def connection(self):
        return self._connection

    def exec(self) :
        with Diagram("Exposed Pod with 3 Replicas", show=False):
            net = Ingress("domain.com") >> Service("svc")
            self.connection >> net
            net >> [Pod("pod1"),
                    Pod("pod2"),
                    Pod("pod3")] << ReplicaSet("rs") << Deployment("dp") << HPA("hpa")