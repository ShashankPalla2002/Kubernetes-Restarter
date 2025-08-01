import json

class ExtractResourceNames:
    def __init__(self, body:json, fields:dict[str, str]):
        self.body = body
        self.fields = fields

    def extractResourcesFromContainers(self, containers, resourceName):
        secret = self.fields.get('secrets', '')
        configmap = self.fields.get('configmaps', '')
        resources = []

        for container in containers:
            for env in container.get('env', []):
                valueFrom = env.get('valueFrom', {})
                print(f"Checking env: {valueFrom}")
                
                if 'secretKeyRef' in valueFrom:
                    print(f"Checking secret: {valueFrom['secretKeyRef'].get('name')} against {secret}")
                    if valueFrom['secretKeyRef'].get('name') == secret:
                        resources.append(resourceName)
                        break
                if 'configMapKeyRef' in valueFrom:
                    if valueFrom['configMapKeyRef'].get('name') == configmap:
                        resources.append(resourceName)
                        break

            for env_from in container.get('envFrom', []):
                if 'secretRef' in env_from:
                    if env_from['secretRef'].get('name') == secret:
                        resources.append(resourceName)
                        break
                if 'configMapRef' in env_from:
                    if env_from['configMapRef'].get('name') == configmap:
                        resources.append(resourceName)
                        break

        return resources

    def extractResourcesFromVolumes(self, volumes, resourceName):
        secret = self.fields.get('secrets', '')
        configmap = self.fields.get('configmaps', '')
        resources = []

        for volume in volumes:
            if volume.get('secret', {}).get('secretName') == secret:
                resources.append(resourceName)
                break
            if volume.get('configMap', {}).get('name') == configmap:
                resources.append(resourceName)
                break

            projected_sources = volume.get('projected', {}).get('sources', [])
            for source in projected_sources:
                if 'secret' in source and source['secret'].get('name') == secret:
                    resources.append(resourceName)
                    break
                if 'configMap' in source and source['configMap'].get('name') == configmap:
                    resources.append(resourceName)
                    break

        return resources

    def extract(self):
        resources = []
        print(self.body.keys())

        for item in self.body.get('items', []):
            metadata = item.get('metadata', {})
            resourceName = metadata.get('name', '')

            if 'template' in item.get('spec', {}):
                podSpec = item.get('spec', {}).get('template', {}).get('spec', {})
            else:
                podSpec = item.get('spec', {})

            containers = podSpec.get('containers', [])
            resources.extend(self.extractResourcesFromContainers(containers, resourceName))

            initContainers = podSpec.get('initContainers', [])
            resources.extend(self.extractResourcesFromContainers(initContainers, resourceName))
            
            volumes = podSpec.get('volumes', [])
            resources.extend(self.extractResourcesFromVolumes(volumes, resourceName))

        return resources