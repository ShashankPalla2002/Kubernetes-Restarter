import json
from pathlib import Path

class ReadMemory:
    def __init__(self):
        self.kresDir = Path.home() / ".kres" / "init"
        self.kresApiFile = self.kresDir / "kresApi.json"

    def readJson(self) -> dict:
        try:
            with open(self.kresDir / "kc.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Kres configuration file not found. Please run 'kres init' to set up the Kres API server.")

        return data
    
    def readKresApiData(self):
        try:
            with open(self.kresApiFile, "r") as f:
                kresApiData = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Kres API configuration file not found. Please run 'kres init' to set up the Kres API server.")
        
        return kresApiData