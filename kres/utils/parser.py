import argparse

class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='kres',
            description="Kubernetes Restarter 'kres' CLI tool"
        )

        self.subParser = self.parser.add_subparsers(
            dest='command',
            required=True
        )

        self.initParser()

    def initParser(self):
        initParser = self.subParser.add_parser(
            "init", help="Initialize with the given kubeconfig"
        )
        initParser.add_argument(
            "-kc", "--kubeconfig",
            help="Path to the kubeconfig file. Default value '~/.kube/config'"
        )

    def parse(self):
        return self.parser.parse_args()