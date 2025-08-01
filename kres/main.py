from kres.subparsers.initParser import InitParser
from kres.subparsers.logoutParser import LogOutParser
from kres.subparsers.apiParser import APIParser
from kres.subparsers.accessParser import AccessParser
from kres.subparsers.restartParser import RestartParser
from kres.utils.parser import Parser

def main():
    args = Parser().parse()

    if args.command == 'init':
        initParser = InitParser()
        initParser.execute(args)

    elif args.command == 'logout':
        logOutParser = LogOutParser()
        logOutParser.execute(args)

    elif args.command == 'api':
        apiParser = APIParser()
        apiParser.execute(args)

    elif args.command == 'access':
        accessParser = AccessParser()
        accessParser.execute(args)

    elif args.command == 'restart':
        print("Restarting resource...")
        restartParser = RestartParser()
        if Parser().validateRestartParser(args):
            restartParser.execute(args)


if __name__ == "__main__":
    main()