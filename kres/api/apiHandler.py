import time
import requests
from datetime import datetime

from kres.utils.readMemory import ReadMemory
from kres.utils.extractResourceNames import ExtractResourceNames

class APIHandler:
    def __init__(self):
        self.readMemory = ReadMemory()
        self.payload = self.generatePayload()     
        
    def isKresApiRunning(self):
        kresApiData = self.readMemory.readKresApiData()
        response = requests.get(f"http://localhost:{kresApiData['port']}/health")
        
        if response.status_code == 200:
            return True
        else:
            return False
        
    def isKubeApiRunning(self):
        url = self.buildURL('/api')

        response = requests.get(
            url=url,
            headers=self.payload.get('headers'),
            verify=self.payload.get('caAuth')
        )

        return response.status_code==200

    def fetchDecryptedToken(self):
        kresApiData = self.readMemory.readKresApiData()
        response = requests.get(
            url = f"http://localhost:{kresApiData['port']}/decrypt"
        )
        
        if response.status_code == 200:
            return response.json().get('token')
        else:
            raise Exception("Failed to fetch decrypted token from Kres API.")

    def generatePayload(self, accept: str = "application/json", contentType: str = "application/json"):
        json  = self.readMemory.readJson()
        token  =  self.fetchDecryptedToken()

        payload = {}
        payload['apiServer'] = json.get('apiServer')
        payload['caAuth']    = json.get('caAuth')
        payload['headers']   = {
            "Authorization": f"Bearer {token}",
            "Accept": accept,
            "Content-Type": contentType
        }

        return payload

    def buildURL(self, path: str):
        return f"{self.payload.get('apiServer')}{path}"

    def checkResourceAccess(self, namespace, resource, verb):
        url = self.buildURL(f'/apis/authorization.k8s.io/v1/selfsubjectaccessreviews')

        headers = self.payload.get('headers')
        caAuth = self.payload.get('caAuth')
        body = {
            "kind": "SelfSubjectAccessReview",
            "apiVersion": "authorization.k8s.io/v1",
            "spec": {
                "resourceAttributes": {
                    "namespace": namespace,
                    "verb": verb,
                    "group": "",
                    "resource": resource
                }
            }
        }

        if resource in ['deployments', 'statefulsets']:
            body['spec']['resourceAttributes']['group'] = 'apps'

        response = requests.post(
            url = url,
            headers = headers,
            json = body,
            verify = caAuth
        )

        if response.status_code in [200, 201]:
            responseData = response.json()
            status = responseData.get('status')
            if status.get('allowed') is True:
                return True
            return False
        else:
            raise Exception(f"Failed to check access for {resource} in namespace {namespace}. Status code: {response.status_code}")
        
    def restartResource(self, namespace, resource, secret:str, configmap:str, reason, name, allFlag):
        if resource == 'deployments':
            url = self.buildURL(f'/apis/apps/v1/namespaces/{namespace}/deployments')

        elif resource == 'statefulsets':
            url = self.buildURL(f'/apis/apps/v1/namespaces/{namespace}/statefulsets')

        elif resource == 'pods':
            url = self.buildURL(f'/api/v1/namespaces/{namespace}/pods')

        headers = self.payload.get('headers')
        caAuth = self.payload.get('caAuth')

        if allFlag:
            response = requests.get(
                url=url,
                headers=headers,
                verify=caAuth
            )
            if response.status_code == 200:
                fields = {
                    'secrets': secret,
                    'configmaps': configmap
                }

                extractResourceNames = ExtractResourceNames(
                    body=response.json(),
                    fields=fields
                )
                resources = extractResourceNames.extract()
                print(f"Found {len(resources)} resources to restart.")

                for resourceName in resources:
                    if resource == 'pods':
                        self.restartPod(url, resourceName)
                    else:
                        self.restartController(url, resourceName, reason)
            else:
                raise Exception(f"Failed to fetch {resource} in namespace {namespace}. Status code: {response.status_code}")
        else:
            if resource == 'pods':
                self.restartPod(url, name)  
            else:
                self.restartController(url, name, reason)
 
        
    def restartController(self, url, name, reason):
        url = f"{url}/{name}"
        restartTriggeredAt = datetime.now().isoformat()
        payload = self.generatePayload(
            contentType="application/strategic-merge-patch+json"
        )

        body = {
            "metadata": {
                "annotations": {
                    "kres.io/restart-reason": reason,
                    "kres.io/restart-triggered-at": str(restartTriggeredAt)
                }
            },

            "spec": {
                "template": {
                    "metadata": {
                        "annotations": {
                            "kres.io/restart-reason": reason,
                            "kres.io/restart-triggered-at": str(restartTriggeredAt)
                        }
                    }
                }
            }
        }

        response = requests.patch(
            url=url,
            headers=payload.get('headers'),
            json=body,
            verify=payload.get('caAuth')
        )

        if response.status_code == 200:
            print(f"Successfully restarted {name}.")
        else:
            raise Exception(f"Failed to restart {name}. Status code: {response.status_code}. Response: {response.text}")
        

    def restartPod(self, url, name):
        url = f"{url}/{name}"
        payload = self.generatePayload()
        
        response = requests.delete(
            url=url,
            headers=payload.get('headers'),
            verify=payload.get('caAuth')
        )

        if response.status_code == 200:
            print(f"Successfully deleted Pod {name}. It will be recreated by the controller.")

        else:
            raise Exception(f"Failed to delete Pod {name}. Status code: {response.status_code}. Response: {response.text}")

