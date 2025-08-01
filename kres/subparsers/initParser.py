import json
from pathlib import Path
from getpass import getpass

from kres.config.extractConfig import ExtractConfig
from kres.utils.checkPortStatus import CheckPortStatus
from kres.api.kresApiLauncher import KresApiLauncher

class InitParser:
    def __init__(self):
        self.kresDir = Path.home() / ".kres" / "init"
        self.kresDir.mkdir(parents=True, exist_ok=True)
        self.port = None

        self.kresApiLauncher = KresApiLauncher()


    def execute(self, args):
        paraphrase = getpass("Provide the paraphrase to encrypt the kubeconfig SA token: ")

        checkPortStatus = CheckPortStatus(args.port) if args.port else CheckPortStatus()
        
        if checkPortStatus.isPortOpen():
            print(f"Port {checkPortStatus.port} is already in use. Please specify a different port or kill the process using that port.")
            return
        
        self.port = checkPortStatus.port

        extractConfig = ExtractConfig(args.kubeconfig) if args.kubeconfig else ExtractConfig()

        inputs = extractConfig.extractConfig()
        token  = extractConfig.extractToken()

        process = self.kresApiLauncher.launchKresApi(
            port=self.port,
            token=token,
            paraphrase=paraphrase
        )
    
        self.storeConfig(inputs)
        self.storeKresApi({"pid": process.pid, "port": self.port})


    def storeConfig(self, inputs):
        with open(self.kresDir / "kc.json", "w") as f:
            json.dump(inputs, f, indent=4)

    def storeKresApi(self, pid):
        with open(self.kresDir / "kresApi.json", "w") as f:
            json.dump(pid, f, indent=4)