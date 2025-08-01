import os
import json
import signal
from pathlib import Path

class StopKresApi:
    def __init__(self):
        self.kresDdir = Path.home() / ".kres" / "init"
        self.kresApiFile = self.kresDdir / "kresApi.json"

        try:
            with open(self.kresApiFile, "r") as f:
                self.kresApiData = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Kres API configuration file not found. Please run 'kres init' to set up the Kres API server.")

    def stop(self):
        try:
            os.kill(self.kresApiData['pid'], signal.SIGTERM)
            print(f"Kres API process (PID {self.kresApiData['pid']}) terminated.")
        except ProcessLookupError:
            print("Process already exited.")