import shutil
from pathlib import Path

class DeleteDir:
    def __init__(self, file_path):
        self.kresDir = Path.home() / ".kres"
        self.dir_path = self.kresDir / file_path

    def delete(self):
        try:
            shutil.rmtree(self.dir_path)
            print(f"Directory {self.dir_path} deleted successfully.")
        except Exception as e:
            print(f"Error deleting directory {self.dir_path}: {e}")