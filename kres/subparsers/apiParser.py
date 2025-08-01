from kres.api.apiHandler import APIHandler

class APIParser:
    def __init__(self):
        pass
        
    def execute(self, args):
        apiHandler = APIHandler()

        if args.type == 'kres':
            if apiHandler.isKresApiRunning():
                print("Kres API is running.")
            else:
                print("Kres API is not running. Please start the Kres API server using kres init command.")

        elif args.type == 'kubernetes':
            if apiHandler.isKubeApiRunning():
                print("Kubernetes API is reachable.")
            else:
                print("Kubernetes API is not reachable. Please check your kubeconfig and network settings.")