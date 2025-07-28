from kres.utils.extractConfig import ExtractConfig
from kres.utils.parser import Parser

def main():
    args = Parser().parse()
    
    if args.kubeconfig == None:
        print(ExtractConfig().extractConfig())
    else:
        print(ExtractConfig(args.kubeconfig).extractConfig())

if __name__ == "__main__":
    main()