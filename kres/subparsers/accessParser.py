from kres.api.apiHandler import APIHandler

class AccessParser:
    def __init__(self):
        self.apiHandler = APIHandler()

    def execute(self, args):
        if self.apiHandler.isKubeApiRunning():
            access = self.apiHandler.checkResourceAccess(
                namespace=args.namespace,
                resource=args.resource,
                verb=args.verb
            )

            if access:
                print(f"Access to {args.resource} in namespace {args.namespace} with verb '{args.verb}' is allowed.")
            else:
                print(f"Access to {args.resource} in namespace {args.namespace} with verb '{args.verb}' is denied.")
        else:
            print("Kubernetes API is not reachable. Please check your kubeconfig and network settings.")