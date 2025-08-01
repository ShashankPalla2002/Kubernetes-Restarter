from kres.config.loadConfig import LoadConfig

class ExtractConfig:
    def __init__(self, kubeConfigPath: str = "~/.kube/config"):
        self.kubeConfigPath = kubeConfigPath
        self.config = LoadConfig(self.kubeConfigPath).loadConfig()

    def extractConfig(self) -> dict[str, str]:

        apiServer   = None
        caAuth      = None
        
        for cluster in self.config['clusters']:
            try:
                apiServer = cluster['cluster']['server']
            except:
                raise ValueError("Missing 'server' key in kubeconfig")
            
            try:
                caAuth = cluster['cluster']['certificate-authority']
            except:
                raise ValueError("Missing 'certificate-authority' key in kubeconfig")

        return {'apiServer': apiServer, 'caAuth': caAuth}
    
    def extractToken(self):

        bearerToken = None

        for user in self.config['users']:
            try:
                bearerToken = user['user']['token']
            except:
                raise ValueError("Missing 'token' key in kubeconfig")
            
        return bearerToken