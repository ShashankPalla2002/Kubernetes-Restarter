from kres.utils.loadConfig import LoadConfig

class ExtractConfig:
    def __init__(self, kubeConfigPath: str = "~/.kube/config"):
        self.kubeConfigPath = kubeConfigPath

    def extractConfig(self) -> dict[str, str]:
        config = LoadConfig(self.kubeConfigPath).loadConfig()

        apiServer = None
        caAuth    = None
        
        for cluster in config['clusters']:
            try:
                apiServer = cluster['cluster']['server']
            except:
                raise ValueError("Missing 'server' key in kubeconfig")
            
            try:
                caAuth = cluster['cluster']['certificate-authority']
            except:
                raise ValueError("Missing 'certificate-authority' key in kubeconfig")

        return {'apiServer': apiServer, 'caAuth': caAuth}