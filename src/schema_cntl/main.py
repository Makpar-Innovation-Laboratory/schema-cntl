import sys
from argparse import ArgumentParser


def parse_cli_args(args):
    parser = ArgumentParser()
    parser.add_argument('action', required = True, help = "Actions: commit, generate")
    parser.add_argument('-str', '--start', help="Starting strand of the revision history")
    parser.add_argument('-end', '--end', action='store_true', help="Ending strand of the revision history")
    return parser.parse_args()


def do_program(args):
    args = parse_cli_args(args)


def entrypoint():
    """Entrypoint for build package
    """
    do_program(sys.argv[1:])


if __name__ == "__main__":
    do_program(sys.argv[1:])
