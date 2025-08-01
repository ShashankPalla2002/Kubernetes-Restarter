import os
import yaml

class LoadConfig:
    def __init__(self, kubeConfigPath: str = "~/.kube/config"):
        self.kubeConfigPath = os.path.expanduser(kubeConfigPath)
    

    def loadConfig(self) -> list:

        if not os.path.exists(self.kubeConfigPath):
            raise FileNotFoundError(f"Kubeconfig not found at: {self.kubeConfigPath}")
        
        with open(self.kubeConfigPath, 'r') as file:
            config = yaml.safe_load(file)

        requiredKeys = ['apiVersion', 'clusters', 'users', 'contexts']

        for key in requiredKeys:
            if key not in config:
                raise ValueError(f"Missing '{key}' in kubeconfig")

        return config