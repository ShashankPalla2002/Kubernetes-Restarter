import subprocess

class KresApiLauncher:
    def __init__(self):
        pass

    def launchKresApi(self, port, token, paraphrase):
        process = subprocess.Popen(
            ["python3", "-m", "kres.api.kresApi", str(port)],  
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        payload = f"{paraphrase}\n{token}\n"
        try:
            process.stdin.write(payload.encode())
            process.stdin.flush()
        except Exception as e:
            print("Failed to pass token/paraphrase to API:", str(e))

        return process