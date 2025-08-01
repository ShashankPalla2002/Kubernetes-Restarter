from kres.api.apiHandler import APIHandler

class RestartParser:
    def __init__(self):
        self.apiHandler = APIHandler()

    def execute(self, args):
        if self.apiHandler.isKubeApiRunning():
            if args.resource == "pods":
                print("⚠️  Warning: Deleting Pods directly is not the recommended way to reload ConfigMaps or Secrets.")
                print("💡 Consider restarting the controller (Deployment/StatefulSet) instead to ensure proper resource reloading.")
                
                userConfirmation = input("Do you want to proceed with deleting the Pods? (y/N): ").strip().lower()

                if userConfirmation != 'y':
                    print("Operation cancelled by the user.")
                    return
                else:
                    access = self.apiHandler.checkResourceAccess(
                        namespace=args.namespace,
                        resource=args.resource,
                        verb="delete"
                    )

            else:                  
                access = self.apiHandler.checkResourceAccess(
                    namespace=args.namespace,
                    resource=args.resource,
                    verb="patch"
                )

            if access:
                self.apiHandler.restartResource(
                    namespace=args.namespace,
                    resource=args.resource,
                    name=args.name,
                    secret=args.secret,
                    configmap=args.configmap,
                    allFlag=args.all,
                    reason=args.reason
                )
            else:
                print(f"You do not have permission to restart {args.resource} in namespace {args.namespace}. Check RBAC policies or your role bindings.")

        else:
            print("Kubernetes API server is not running or not reachable.")
