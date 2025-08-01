from kres.utils.checkKresApiStatus import CheckKresApiStatus
from kres.utils.stopKresApi import StopKresApi
from kres.utils.deleteDir import DeleteDir

class LogOutParser:
    def __init__(self):
        if not CheckKresApiStatus().isKresApiRunning():
            print("Kres API is not running. Please login first.")
            return

        self.stopKresApi = StopKresApi()
        self.deleteDir = DeleteDir("init")

    def execute(self, args):
        self.stopKresApi.stop()
        self.deleteDir.delete()